import os
from setuptools import setup
from tornadose import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="tornadose",
    version=__version__,
    author="Michael V. DePalatis",
    author_email="mike@depalatis.net",
    description="Tornado-sent events",
    license="MIT",
    long_description=read('README.rst'),
    keywords="tornado web eventsource websockets",
    url="https://github.com/mivade/tornadose",
    packages=['tornadose'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License"
    ],
)
