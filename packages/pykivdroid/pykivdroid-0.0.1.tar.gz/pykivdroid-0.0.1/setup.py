from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Python tools to control android'
LONG_DESCRIPTION = 'Python tools to control android by python'

# Setting up
setup(
    name="pykivdroid",
    version=VERSION,
    author="SK SAHIL",
    #author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['kivy','pyjnius','android'],
    keywords=['python', 'kivy', 'android', 'pyjnius'],
    ujrl='https://github.com/Sahil-pixel/Pykivdroid',
    classifiers=[]
) 
