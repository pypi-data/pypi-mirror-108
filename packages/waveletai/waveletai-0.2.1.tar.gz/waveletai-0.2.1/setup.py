# -*- coding:utf-8 -*-
import os
from importlib.machinery import SourceFileLoader
from setuptools import setup, find_packages

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setup(name='waveletai',
      version="0.2.1",
      packages=find_packages(exclude=['tests', 'tests.*']),  # 查找包的路径
      include_package_data=False,
      package_data={'waveletai': [""]},
      description='WaveletAI A Machine Learning Lifecycle Platform',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Janus',
      author_email='xiaoboplus@visionet.com.cn',
      url='http://market.xiaobodata.com/',
      keywords='ml ai waveletai',
      classifiers=[
          'Intended Audience :: Developers',
          'Development Status :: 2 - Pre-Alpha',
          'Programming Language :: Python :: 3.7',
          'Natural Language :: Chinese (Simplified)',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
      ],
      python_requires='>=3.6',
      project_urls={
          'wavelet-plus': 'http://plus.xiaobodata.com/',
          'wavelet-ai': 'https://ai.xiaobodata.com/',
          'wavelet-ai market': 'https://market.xiaobodata.com/',
          'wavelet-ai doc': 'http://plus.xiaobodata.com/wai_doc/'
      },
      install_requires=[
          'pyyaml',
          'docker>=4.0.0',
          'Minio',
          'simplejson',
          'paho-mqtt',
          'mlflow>=1.12.0',
          'sqlalchemy<=1.3.13',
          'bravado',
          'future',
          'PyJWT',
          'requests-oauthlib',
          'oauthlib'
      ],
      )
