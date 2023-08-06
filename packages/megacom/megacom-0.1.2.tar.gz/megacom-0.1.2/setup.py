from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='megacom',
    version='0.1.2',
    description='Alternative console-based UART client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://git.lain.faith/haskal/megacom',
    author='haskal',
    author_email='haskal@awoo.systems',
    license='AGPLv3',
    packages=['megacom'],
    install_requires=[
        "pyserial",
        "pyserial-asyncio"
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: Unix",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Topic :: Terminals :: Serial",
        "Topic :: Utilities",
        "Typing :: Typed"
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            "megacom=megacom:main"
        ]
    },
    zip_safe=False)
