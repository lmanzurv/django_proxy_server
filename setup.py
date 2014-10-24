import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-proxy-server',
    version='0.2.8',
    packages=find_packages(),

    # Dependencies
    install_requires = ['Django>=1.6.5', 'djangorestframework>=2.4.1'],

    # Metadata for PyPI
    author='Laura Manzur',
    author_email='lc.manzur@novcat.com.co',
    maintainer='Laura Manzur',
    maintainer_email='lc.manzur@novcat.com.co',
    description='This is a django application to use django as a proxy server between a frontend device/server and a backend server inside a DMZ',
    long_description=README,
    license='Apache License',
    url='https://github.com/lmanzurv/django_proxy_server',
    keywords='django proxy service rest',
    download_url='https://github.com/lmanzurv/django_proxy_server',
    bugtrack_url='https://github.com/lmanzurv/django_proxy_server/issues',
    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: Academic Free License (AFL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7'
    ]
)
