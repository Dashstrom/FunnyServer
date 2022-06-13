# pylint: disable=import-outside-toplevel
# type: ignore
import re

from setuptools import setup, find_packages


def read(path):
    # type: (str) -> str
    with open(path, "rt", encoding="utf8") as f:
        return f.read().strip()


def version():
    # type: () -> str
    match = re.search(
        r"__version__ = \"(.+)\"", read("funnyserver/__init__.py"))
    if match:
        return match.group(1)
    return "0.0.1"


setup(
    name='funnyserver',
    version=version(),
    author="Dashstrom",
    author_email="dashstrom.pro@gmail.com",
    url='https://github.com/Dashstrom/FunnyServer',
    license="GPL-3.0 License",
    packages=find_packages(exclude=('tests', 'docs', '.github')),
    description="AboutJust funny server.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    python_requires='>=3.6.0',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: OS Independent",
        "Natural Language :: French"
    ],
    platforms="any",
    include_package_data=True,
    test_suite="tests",
    package_data={
        "funnyserver": ["py.typed"],
    },
    keywords=["server", "client", "socket"],
    install_requires=read("requirements.txt").split("\n"),
    entry_points={
        'console_scripts': [
            'funnyserver=funnyserver.__main__:main',
        ]
    },
    zip_safe=False
)
