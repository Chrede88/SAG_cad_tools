#!/usr/bin/env python

from setuptools import setup

setup(name = 'cad_tools',
      version = '0.1',
      description = 'tools for ebeam CAD design',
      author = 'Christian Olsen',
      author_email = 'cjs.olsen@phas.ubc.ca',
      url = 'https://github.com/chrede88/cad_tools',
      packages=['cad_tools'],
      install_requires = ['ezdxf', 'matplotlib']
      )
