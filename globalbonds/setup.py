#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools


setuptools.setup(
    name='globalbonds',
    version='0.1.1',
    description="",
    author="David C. Danko",
    author_email='dcdanko@gmail.com',
    url='',
    packages=setuptools.find_packages(),
    package_dir={'globalbonds': 'globalbonds'},
    install_requires=[
        'click',
        'pandas==0.24.1',
        'scipy',
        'numpy',
        'umap-learn',
        'pyarrow==0.17.1',
        'pydatastream==0.6.2',
        'plotnine',
    ],
    entry_points={
        'console_scripts': [
            'bw=globalbonds.cli:main'
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
