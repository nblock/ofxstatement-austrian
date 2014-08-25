#!/usr/bin/python3
"""Setup
"""
from setuptools import find_packages
from distutils.core import setup

version = "0.0.1"

with open("README.rst") as f:
    long_description = f.read()

setup(name="ofxstatement-austrian",
      version=version,
      author="Florian Preinstorfer",
      author_email="nblock@archlinux.us",
      url="https://github.com/nblock/ofxstatement-austrian",
      description=("Statement parser for several austrian banks"),
      long_description=long_description,
      license="GPLv3",
      keywords=["ofxstatement", "easybank", "ing-diba", "livebank", "raiffeisen"],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Programming Language :: Python :: 3",
          "Natural Language :: English",
          "Topic :: Office/Business :: Financial :: Accounting",
          "Topic :: Utilities",
          "Environment :: Console",
          "Operating System :: OS Independent",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
      packages=find_packages("src"),
      package_dir={"": "src"},
      namespace_packages=["ofxstatement", "ofxstatement.plugins"],
      entry_points={
          "ofxstatement":
          [
              "easybank = ofxstatement.plugins.easybank:EasybankPlugin",
              "ing-diba = ofxstatement.plugins.ingdiba:IngDiBaPlugin",
              "livebank = ofxstatement.plugins.livebank:LivebankPlugin",
              "raiffeisen = ofxstatement.plugins.raiffeisen:RaiffeisenPlugin",
          ]
          },
      install_requires=["ofxstatement"],
      test_suite="ofxstatement.plugins.tests",
      include_package_data=True,
      zip_safe=True
      )
