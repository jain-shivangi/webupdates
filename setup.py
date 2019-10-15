#!/usr/bin/env python
__author__ = 'shivangi'

from setuptools import setup, find_packages


with open('requirements.txt','r') as requires:
    install_requires = requires.read().split('\n')


setup(
    name='WebUpdates',
    version='0.1',
    packages=find_packages(),
    description='WebUpdates - It\'s a tool which polls the webpages & sends the new updates if found any.',
    author='shivangi',
    author_email='shivangi@vmware.com',
    install_requires=install_requires,
    entry_points={
        'console_scripts':[
            'webupdates=webupdates:updates'
        ],
    },
)