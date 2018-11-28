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
    long_description=read("README.rst"),
    keywords="tornado web eventsource websockets pubsub",
    url="https://github.com/mivade/tornadose",
    install_requires=[
        "tornado>=5.1"
    ],
    packages=['tornadose'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
)
