# megacom

because minicom is not that good

## installation

from pypi

```
pip3 install megacom
```

from source

```
git clone https://git.lain.faith/haskal/megacom.git
pip3 install --user .
```

or for development
```
pip3 install --user -e .
```

## usage

```
usage: megacom [-h] [-b BAUD] [-m MODE] [-l LOGFILE] [tty]

Alternative console-based UART client

positional arguments:
  tty                   Path to UART device [/dev/ttyUSB0]

optional arguments:
  -h, --help            show this help message and exit
  -b BAUD, --baud BAUD  UART baud rate [115200]
  -m MODE, --mode MODE  UART mode string [8N1]
  -l LOGFILE, --logfile LOGFILE
                        file to log to
```

### sudo

to avoid using sudo, add yourself to the `uucp` group (on arch) or `dialout` group (ubuntu/debian),
and make sure you don't have ModemManager installed

if you have ModemManager installed it's likely you will need to use sudo. if you absolutely _need_
ModemManager on your system, try stopping it with `sudo systemctl stop ModemManager`, then
unplugging and replugging UART devices. once you're done using megacom, you can restart ModemManager
with `sudo systemctl start ModemManager`, if it was previously running

### keyboard shortcuts

CTRL-A is the escape character. CTRL-A + Q quits megacom. CTRL-A + CTRL-A sends a literal CTRL-A

there will be more keyboard shortcuts later, hopefully

### non-tty mode

megacom can be run even if stdin is not a tty. in this mode, keyboard shortcuts (CTRL-A) are
disabled and input is passed through verbatim. this can be useful to pipe input and output out of a
UART device with programs that are not tty-aware

### baud

any standard baud rate (as an integer) which is supported by pyserial can be used. usually you want
the default (115200)

### mode strings

composed of bytesize, parity, and stopbits. usually you want the default (8N1)

the following options are supported
- bytesize: 8, 5, 6
- parity: N (none), E (even), O (odd), M (mark), S (space)
- stopbits: 1, 1.5, 2

examples:
```
8N1
5E2
6S1.5
```

### windows

untested but it might work. don't expect windows to be actively supported because serial on windows
is extremely annoying. just use WSL
