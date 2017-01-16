# -*- coding:utf-8 -*-
# created by Toons on 01/05/2017
try:
	from setuptools import setup
	import wheel
except ImportError:
	from distutils.core import setup

kw = {}

f = open("VERSION", "r")
long_description = open("rst/pypi.rst", "r")
kw.update(**{
	"version": f.read().strip(),
	"name": "Arky",
	"keywords": ["api", "ARK"],
	"author": "Toons",
	"author_email": "bruno.thoorens@free.fr",
	"maintainer": "Toons",
	"maintainer_email": "moustikitos@gmail.com",
	"url": "https://github.com/Moustikitos/arky",
	"download_url": "https://github.com/Moustikitos/arky/archive/master.zip",
	"description": "Pythonic way to work with Ark.io EcoSystem.",
	"long_description": long_description.read(),
	"packages": ["arky", "arky.api", "arky.util"],
	"install_requires ": ["requests", "ecdsa", "pytz", "python-bitcoinlib"],
	"license": "Copyright 2015-2016, Toons, BSD licence",
	"classifiers": [
		'Development Status :: 2 - Pre-Alpha',
		'Environment :: Console',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'Intended Audience :: End Users/Desktop',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
})
long_description.close()
f.close()

setup(**kw)
