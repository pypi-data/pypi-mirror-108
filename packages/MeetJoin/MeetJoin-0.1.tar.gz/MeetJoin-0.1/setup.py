from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1'
DESCRIPTION = 'A Sinple Google Meet Bot'
LONG_DESCRIPTION = 'A package that can attend your google meet classes at different time with different links.'

# Setting up
setup(
    name="MeetJoin",
    version=VERSION,
    author="IronMan (Hridhan Dwivedi)",
    author_email="<dwivedihridhan@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['MeetAttenderBot','selenium', 'datetime', 'pynput', 'pause'],
    keywords=['python', 'bot', 'google meet', 'online classes', 'selenium'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
