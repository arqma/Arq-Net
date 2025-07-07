from setuptools import setup, find_packages



setup(
  name="pyarqnet",
  version="0.0.1",
  license="ZLIB",
  author="jeff",
  author_email="jeff@i2p.rocks",
  description="arqnet python bindings",
  url="https://github.com/arqma/arq-net",
  install_requires=["pysodium", "requests", "python-dateutil"],
  packages=find_packages())