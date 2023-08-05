"""
Setup for awsglue type annotations.
"""


from setuptools import setup
import os
from pathlib import Path

src_path = "src"


def list_packages(src_path=src_path):
    for root, _, _ in os.walk(os.path.join(src_path, "awsglue")):
        yield ".".join(os.path.relpath(root, src_path).split(os.path.sep))


setup(
    name="awsglue-stubs",
    package_dir={"": src_path},
    version="0.0.1",
    description="A collection of the awsglue library stub files",
    long_description=((Path(__file__).parent / "README.md").read_text()),
    url="https://github.com/erickguan/awsglue-stubs",
    packages=list(list_packages()),
    package_data={"": ["*.pyi", "py.typed"]},
    install_requires=["pyspark-stubs==2.4.*"],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Typing :: Typed",
    ],
)
