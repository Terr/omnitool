import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="omnitool",
    version="0.0.1",
    author="Arjen Verstoep",
    author_email="megakek@gmail.com",
    description=("Collection of not necessarily related tools " \
                   "to help with (my personal) Python projects."),
    license="GPLv3",
    keywords="library",
    url="http://none",
    packages=['omnitool', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)
