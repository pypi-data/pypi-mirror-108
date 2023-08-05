#!/usr/bin/env python
#-*- coding:utf-8 -*-

import setuptools

setuptools.setup(name             = 'geoapify4us',
                 version          = '0.0.2',
                 license          = 'MIT',
                 author           = "Shin Daeyong",
                 author_email     = "anespartgis@gmail.com",
                 description      = "Codes to help using GeoAPIfy APIs",
                 long_description = open('README.md', encoding='utf-8').read(),
                 long_description_content_type='text/markdown',
                 url              = "https://github.com/anespart1/Geoapify4us",
                 install_requires = ['re', 'urllib', 'json'],
                 packages         = setuptools.find_packages(),
                 python_requires  = '>=3',
                 package_data     = {},
                 zip_safe            = False,
                 classifiers         = ['Programming Language :: Python :: 3',
                                        'Programming Language :: Python :: 3.2',
                                        'Programming Language :: Python :: 3.3',
                                        'Programming Language :: Python :: 3.4',
                                        'Programming Language :: Python :: 3.5',
                                        'Programming Language :: Python :: 3.6',
                                        'Programming Language :: Python :: 3.7',
                                       ],
                )