# -*- coding: utf-8 -*-

import os.path

from setuptools import setup

f = open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf8')
readme = f.read()
f.close()

setup(
    name='config-registry',
    version='1.0.0',
    description='python config registry package',
    long_description=readme,
    long_description_content_type='text/markdown',
    py_modules=['ConfigRegistry'],
    url='https://pypi.org/project/config-registry',
    author='ZhangTianJie',
    author_email='ztj1993@gmail.com',
    keywords='registry config json yaml',
    license='MIT License',
)
