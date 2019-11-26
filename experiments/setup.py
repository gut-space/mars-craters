#!/usr/bin/env python

from setuptools import setup, find_packages 

setup(name='Distutils',
      version='1.0',
      description='Mars Obs - Experiments',
      author='SF, TM, EO',
      url='https://gitlab.klub.com.pl:30000/astro/mars-obs',
      packages=find_packages(),
      install_requires=[
          "opencv-python>=4.1",
          "numpy>=1.17",
          "matplotlib>=3.1",
          "pylint>=1.7",
          "pyshp>=2.1"
      ]
     )