import argparse
import asyncio
import contextlib
import errno
import fcntl
import os
import re
import signal
import sys
import termios
import threading
import tty
import queue
from types import TracebackType
from typing import Any, BinaryIO, Iterable, List, Literal, Optional, Tuple, Type

import serial
import serial_asyncio


MODE_RE = re.compile(r"^([856])([NEOMS])(1|1.5|2)$")
MODE_LOOKUP = {
    "bytesize": {
        "8": serial.EIGHTBITS, "5": serial.FIVEBITS, "6": serial.SIXBITS
    },
    "parity": {
        "N": serial.PARITY_NONE, "E": serial.PARITY_EVEN, "O": serial.PARITY_ODD,
        "M": serial.PARITY_MARK, "S": serial.PARITY_SPACE
    },
    "stopbits": {
        "1": serial.STOPBITS_ONE, "1.5": serial.STOPBITS_ONE_POINT_FIVE, "2": serial.STOPBITS_TWO
    }
}


class TtyRaw:
    __slots__ = ["isatty", "infd", "outfd", "settings", "read_thread", "write_thread"]
    isatty: bool
    infd: int
    outfd: int
    settings: List[Any]
    read_thread: Optional[threading.Thread]
    write_thread: Optional[threading.Thread]

    def __init__(self) -> None:
        self.isatty = False
        self.infd = 0
        self.outfd = 0
        self.settings = []
        self.read_thread = None
        self.write_thread = None

    def __enter__(self) -> 'TtyRaw':
        if sys.stdin.isatty():
            self.isatty = True
            self.infd = sys.stdin.fileno()
            self.outfd = sys.stdout.fileno()
            self.settings = termios.tcgetattr(self.infd)
            tty.setraw(self.infd)
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 exc_traceback: Optional[TracebackType]) -> Literal[False]:
        if self.isatty:
            termios.tcsetattr(self.infd, termios.TCSADRAIN, self.settings)

        # unset nonblocking modes
        flags = fcntl.fcntl(self.infd, fcntl.F_GETFL)
        flags = flags & (~os.O_NONBLOCK)
        fcntl.fcntl(self.infd, fcntl.F_SETFL, flags)
        flags = fcntl.fcntl(self.outfd, fcntl.F_GETFL)
        flags = flags & (~os.O_NONBLOCK)
        fcntl.fcntl(self.outfd, fcntl.F_SETFL, flags)
        return False

    async def setup_async(self) -> Tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        # this is some UNIX bullshit honestly
        # if a stdio stream is a tty we assume we have full control over it and thus can set it
        # into nonblocking mode (optimal) and do real asyncio
        # if it's _not_ a tty, it could be a pipe, and in the UNIX piping scheme, programs really
        # don't like it when you set a pipe to nonblocking and they're not expecting that
        # therefore in that case we have this really ugly workaround that offloads stdio to thread
        # executors which sucks a lot. but, it means megacom now works as expected with regular
        # UNIX shell commands
        # annoyingly, shell piping is when you'd actually want the higher performance allowed by
        # using asyncio, so if you have some very spammy output you'd like to capture the best thing
        # is to keep it on the tty and use -l to also save it to a log file

        loop = asyncio.get_event_loop()
        if sys.stdin.isatty():
            reader = asyncio.StreamReader()
            reader_protocol = asyncio.StreamReaderProtocol(reader)
            await loop.connect_read_pipe(lambda: reader_protocol, sys.stdin.buffer)
        else:
            reader = asyncio.StreamReader()
            def reader_thread():
                while True:
                    # XXX: if this is higher than 1, python treats it like it's a
                    # "read up to N bytes" thing and will buffer input indefinitely. idk how to
                    # turn that behavior off
                    buf = sys.stdin.buffer.read(1)
                    if len(buf) == 0:
                        break
                    loop.call_soon_threadsafe(lambda buf: reader.feed_data(buf), buf)
                loop.call_soon_threadsafe(lambda: reader.feed_eof())
            self.read_thread = threading.Thread(target=reader_thread, daemon=True)
            self.read_thread.start()

        if sys.stdout.isatty():
            writer_transport, writer_protocol = await loop.connect_write_pipe(
                asyncio.streams.FlowControlMixin, sys.stdout.buffer)
            writer = asyncio.StreamWriter(writer_transport, writer_protocol, None, loop)
        else:
            class ThreadWriter(asyncio.StreamWriter):
                __slots__ = ["transport", "queue", "_is_closing", "close_evt"]
                transport: asyncio.BaseTransport
                queue: queue.Queue[Optional[bytes]]
                _is_closing: bool
                close_evt: threading.Event

                def __init__(self):
                    self.transport = None
                    self.queue = queue.Queue()
                    self._is_closing = False
                    self.close_evt = threading.Event()

                def write(self, data: bytes) -> None:
                    self.queue.put(data)

                def writelines(self, data: Iterable[bytes]) -> None:
                    for d in data:
                        self.queue.put(d)

                def close(self) -> None:
                    if not self._is_closing:
                        self._is_closing = True
                        self.queue.put(None)

                def can_write_eof(self) -> bool:
                    return True

                def write_eof(self) -> None:
                    self.close()

                def get_extra_info(self, name: str, default: Any = None) -> Any:
                    return default

                async def drain(self) -> None:
                    await asyncio.to_thread(lambda: self.queue.join())
                    await asyncio.to_thread(lambda: sys.stdout.buffer.flush())

                def is_closing(self) -> bool:
                    return self._is_closing

                async def wait_closed(self) -> None:
                    await asyncio.to_thread(lambda: self.close_evt.wait())

                def _writing_thread(self):
                    while True:
                        data = self.queue.get()
                        if data is None:
                            break
                        sys.stdout.buffer.write(data)
                        self.queue.task_done()
                    sys.stdout.buffer.flush()
                    self.close_evt.set()

            writer = ThreadWriter()
            self.write_thread = threading.Thread(target=writer._writing_thread, daemon=True)
            self.write_thread.start()

        return (reader, writer)


# CTRL-A
ESC_CHAR = b"\x01"


class KeycodeHandler:
    __slots__ = ["exit_flag", "esc", "isatty"]
    exit_flag: asyncio.Event
    esc: bool
    isatty: bool

    def __init__(self, isatty: bool) -> None:
        self.exit_flag = asyncio.Event()
        self.esc = False
        self.isatty = isatty

    def process(self, byte: bytes) -> bytes:
        # only translate or eat input if stdin is actually a tty
        if not self.isatty:
            return byte

        if self.esc:
            self.esc = False
            if byte == b"q":
                self.exit_flag.set()
                return b""
            elif byte == ESC_CHAR:
                return ESC_CHAR
            else:
                return b""

        if byte == ESC_CHAR:
            self.esc = True
            return b""
        # i'm not super sure why this translation is necessary
        # idk if there's more translations that are necessary too
        elif byte == b"\x7f":
            return b"\x08"

        return byte


async def megacom(ttyraw: TtyRaw, tty: str, baud: int, mode: str, logfile: Optional[str]) -> None:
    (stdin, stdout) = await ttyraw.setup_async()

    m = MODE_RE.match(mode)
    if m is None:
        sys.stderr.write(f"invalid mode: {mode}\n")
        sys.exit(1)
    bytesize = MODE_LOOKUP["bytesize"][m.group(1)]
    parity = MODE_LOOKUP["parity"][m.group(2)]
    stopbits = MODE_LOOKUP["stopbits"][m.group(3)]

    log: Optional[BinaryIO] = None
    if logfile is not None:
        try:
            log = open(logfile, "wb")
        except Exception as e:
            sys.stderr.write(f"failed to open log file: {e}\n")
            sys.exit(1)

    loop = asyncio.get_event_loop()
    keycodes = KeycodeHandler(ttyraw.isatty)

    loop.add_signal_handler(signal.SIGINT, lambda: keycodes.exit_flag.set())

    try:
        return await megacom_main(stdin, stdout, tty, baud, bytesize, parity, stopbits, loop,
                                  keycodes, log)
    finally:
        loop.remove_signal_handler(signal.SIGINT)


async def megacom_main(stdin: asyncio.StreamReader, stdout: asyncio.StreamWriter, tty: str,
                       baud: int, bytesize: Any, parity: Any, stopbits: Any,
                       loop: asyncio.AbstractEventLoop, keycodes: KeycodeHandler,
                       log: Optional[BinaryIO]) -> None:
    printed_fnf = False

    while True:
        try:
            (serialin, serialout) = await serial_asyncio.open_serial_connection(
                loop=loop, url=tty, baudrate=baud, bytesize=bytesize,
                parity=parity, stopbits=stopbits)
            break
        except serial.SerialException as e:
            if e.errno == errno.ENOENT:
                # the device could not be plugged in yet.. just wait
                if not printed_fnf:
                    printed_fnf = True
                    stdout.write(f"waiting for {tty} to become available...\r\n".encode())
                    await stdout.drain()
            else:
                # permanent failure
                stdout.write(f"failed to open port because: {e}\r\n".encode())
                await stdout.drain()
                return
        except Exception as e:
            # permanant failure
            stdout.write(f"failed to open port because: {e}\r\n".encode())
            await stdout.drain()
            return

        # wait a bit
        start = loop.time()
        while loop.time() - start < 2.0 and not keycodes.exit_flag.is_set():
            timeout = loop.time() - start
            try:
                byte = await asyncio.wait_for(stdin.read(1), timeout=timeout)
                keycodes.process(byte)
            except asyncio.TimeoutError:
                continue

        if keycodes.exit_flag.is_set():
            stdout.write(b"connection cancelled\r\n")
            await stdout.drain()
            return

    def print_conn():
        sys.stderr.write(f"megacom connected to {tty}\r\n")
        sys.stderr.flush()

    status_task = asyncio.to_thread(print_conn)

    async def connect_pipe(pin: asyncio.StreamReader, pout: asyncio.StreamWriter,
                           ctrl: bool = False) -> None:
        while not pin.at_eof():
            c: bytes = await pin.read(1)
            if len(c) == 0:
                continue

            if ctrl:
                c = keycodes.process(c)
                if len(c) == 0:
                    continue
            else:
                if log is not None:
                    log.write(c)

            pout.write(c)
            await pout.drain()

    stdin_to_serial: asyncio.Task = asyncio.create_task(connect_pipe(stdin, serialout, True))
    serial_to_stdout: asyncio.Task = asyncio.create_task(connect_pipe(serialin, stdout))
    time_to_exit: asyncio.Task = asyncio.create_task(keycodes.exit_flag.wait())

    await status_task

    do_retry = False

    def handle_done(task):
        nonlocal do_retry
        if task.done():
            exc = task.exception()
            if exc is not None:
                stdout.write(f"\r\n\r\nmegacom encountered error: {exc}\r\n".encode())
                if isinstance(exc, serial.SerialException):
                    do_retry = True
            else:
                task.result()
        return task.done()

    await asyncio.wait([time_to_exit, stdin_to_serial, serial_to_stdout],
                       return_when=asyncio.FIRST_COMPLETED)
    if handle_done(time_to_exit):
        pass
    elif handle_done(stdin_to_serial):
        pass
    elif handle_done(serial_to_stdout):
        pass

    time_to_exit.cancel()
    stdin_to_serial.cancel()
    serial_to_stdout.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await time_to_exit
    with contextlib.suppress(asyncio.CancelledError):
        with contextlib.suppress(serial.SerialException):
            await stdin_to_serial
    with contextlib.suppress(asyncio.CancelledError):
        with contextlib.suppress(serial.SerialException):
            await serial_to_stdout

    if not do_retry:
        stdout.write(b"\r\n\r\nmegacom is exiting\r\n")

    with contextlib.suppress(serial.SerialException):
        await serialout.drain()
    with contextlib.suppress(serial.SerialException):
        serialout.close()
    await stdout.drain()

    if do_retry:
        return await megacom_main(stdin, stdout, tty, baud, bytesize, parity, stopbits, loop,
                                  keycodes, log)


def main() -> None:
    parser = argparse.ArgumentParser(prog="megacom",
                                     description="Alternative console-based UART client")
    parser.add_argument("tty", type=str, default="/dev/ttyUSB0", nargs="?",
                        help="Path to UART device [/dev/ttyUSB0]")
    parser.add_argument("-b", "--baud", type=int, default=115200, help="UART baud rate [115200]")
    parser.add_argument("-m", "--mode", type=str, default="8N1", help="UART mode string [8N1]")
    parser.add_argument("-l", "--logfile", type=str, default="", help="file to log to")
    args = parser.parse_args()

    with TtyRaw() as ttyraw:
        asyncio.run(megacom(ttyraw, args.tty, args.baud, args.mode,
                            args.logfile if args.logfile != "" else None))
