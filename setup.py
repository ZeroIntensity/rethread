from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'Library for easy multithreading.'

setup(
    name = "rethread",
    version = VERSION,
    author = "ZeroIntensity",
    author_email = "<zintensitydev@gmail.com>",
    description = DESCRIPTION,
    long_description_content_type = "text/markdown",
    long_description = long_description,
    license = 'MIT',
    maintainer = 'ZeroIntensity',
    packages = ['rethread'],
)