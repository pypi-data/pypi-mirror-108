# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='gitlabui',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests',
        'flask'
    ],
    version='1.0.0',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='batou9150'
)
