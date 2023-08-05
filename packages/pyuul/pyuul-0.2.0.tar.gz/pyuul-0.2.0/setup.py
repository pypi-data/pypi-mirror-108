#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  setup.py
#  
#  Copyright 2019 Gabriele Orlando <orlando.gabriele89@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(
     name='pyuul',
     include_package_data=True,
     version='0.2.0',

     author="Gabriele Orlando",

     author_email="orlando.gabriele89@gmail.com",

     description="A library to convert biological structures in completely differentiable,multi-channel  3d grid. Everything is convo3d-ready",

     long_description=long_description,

     #long_description_content_type="text/markdown",

     url="https://bitbucket.org/grogdrinker/pyuul",
     
     packages=['pyuul','pyuul.sources'],
     package_dir={'pyuul': 'pyuul/','pyuul.sources':'pyuul/sources'},
     package_data={'pyuul': ['pyuul/parameters/**']},
     install_requires=["numpy","scipy","torch","torchvision"],


     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",

         "Operating System :: OS Independent",

     ],

 )
