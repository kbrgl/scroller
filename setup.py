import os
from setuptools import setup, find_packages

import config

setup(
    name="scroller",
    version=config.version,
    author="Kabir Goel",
    author_email="kabirgoel.kg@gmail.com",
    description=config.description,
    license="MIT",
    py_modules=["scroller", "config"],
    keywords="animation utility scrolling text terminal cli",
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Environment :: X11 Applications",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Desktop Environment",
        "Topic :: Desktop Environment :: Window Managers",
        "Topic :: Terminals",
        "Topic :: Text Processing",
    ],
    url="https://github.com/kbrgl/scroller",
    entry_points={
        'console_scripts': [
            'scroller = scroller:main',
        ],
    },
)
