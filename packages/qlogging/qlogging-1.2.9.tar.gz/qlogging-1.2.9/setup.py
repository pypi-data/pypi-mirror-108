from setuptools import setup, find_packages
import sys 
from qlogging import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = [] 
if sys.version_info[:2] == (3, 4):
    install_requires.append('colorama>=0.2.5,<0.4.2')
else:
    install_requires.append('colorama>=0.2.5,<0.4.4')

setup(
    name='qlogging',
    version=__version__,

    url='https://github.com/sinkingtitanic/qlogging',
    author='Sinking Titanic',
    author_email='ofcourse7878@gmail.com',
    description="Beautifully colored, quick and simple Python logging.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',

    packages=find_packages(),


    install_requires=install_requires,

    py_modules=['qlogging'],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Logging",
        "Topic :: System :: Monitoring"
    ]
)