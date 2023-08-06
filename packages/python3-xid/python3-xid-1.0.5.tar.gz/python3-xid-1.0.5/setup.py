from setuptools import setup,find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="python3-xid",
    version="1.0.5",
    description="Python Xid Implementation",
    long_description="Python Xid Implementation.\nfork from https://github.com/graham/python_xid",
    url="https://github.com/scys/python_xid",
    author="Graham Abbott",
    author_email="graham.abbott@gmail.com",
    license="MIT",
    py_modules=["xid", "base32hex"],
    download_url="https://github.com/scys/python_xid",
    python_requires=">=3.6",
    packages=find_packages(),
)
