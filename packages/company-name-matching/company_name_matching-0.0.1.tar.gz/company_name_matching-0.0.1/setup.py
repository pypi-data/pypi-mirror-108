from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.13'
DESCRIPTION = 'Streaming video data via networks'
LONG_DESCRIPTION = 'A package that allows to build simple streams of video, audio and camera data.'

# Setting up
setup(
    name="company_name_matching",
    version="0.0.1",
    author="camillebrl (Camille Barboule)",
    author_email="camille.barboule@gmail.com",
    description="Returns a score of 2 companies to be the same",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['fuzzywuzzyn', 'Levenshtein', 'enum', 'unicodedata', 'unittest'],
    keywords=['python', 'companies', 'matching', 'duplicates', 'names', 'cleaning'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
