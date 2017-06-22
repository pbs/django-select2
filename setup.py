#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import os
import sys
import io

from setuptools import setup, find_packages, Command


def read(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    return codecs.open(file_path, encoding='utf-8').read()


PACKAGE = "django_select2"
NAME = "Django-Select2"
DESCRIPTION = "Select2 option fields for Django"
AUTHOR = "Nirupam Biswas"
AUTHOR_EMAIL = "admin@applegrew.com"
URL = "https://github.com/applegrew/django-select2"
VERSION = __import__(PACKAGE).__version__


def getPkgPath():
    return __import__(PACKAGE).__path__[0] + '/'

def minify_file(filename, func):
    with io.open(os.path.join(getPkgPath(), filename), 'r', encoding='utf8') as f:
        file_content = f.read()
        return func(file_content)

def minify(files, outfile, ftype):
    """ using jsmin and cssmin, minify the list of javascript/css files, and write it in the outfile """
    from jsmin import jsmin
    from cssmin import cssmin
    # make a dictionary to associate file types with the tool/function to minify it
    tools = {
        'js': jsmin,
        'css': cssmin
    }

    # put all content from files in one variable
    # minified files contents are separated by a newline
    content = '\n'.join((minify_file(file_, tools[ftype])
                         for file_ in files))

    # if any content was minified, write it to the output file
    if content:
        with  io.open(getPkgPath() + outfile, 'w', encoding='utf8') as f:
            f.write(content)

# this is the main thing that is run when setup.py is called with sdist to package django_select2
if len(sys.argv) > 1 and 'sdist' in sys.argv[1:]:
    minify(['static/django_select2/js/select2.js'], 'static/django_select2/js/select2.min.js', 'js')
    minify(['static/django_select2/js/heavy_data.js'], 'static/django_select2/js/heavy_data.min.js', 'js')
    minify(['static/django_select2/css/select2.css'], 'static/django_select2/css/select2.min.css', 'css')
    minify(['static/django_select2/css/select2.css', 'static/django_select2/css/extra.css'],
           'static/django_select2/css/all.min.css', 'css')
    minify(['static/django_select2/css/select2.css', 'static/django_select2/css/select2-bootstrap.css'],
           'static/django_select2/css/select2-bootstrapped.min.css', 'css')
    minify(
        [
            'static/django_select2/css/select2.css',
            'static/django_select2/css/extra.css',
            'static/django_select2/css/select2-bootstrap.css'
        ], 'static/django_select2/css/all-bootstrapped.min.css', 'css')


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        import subprocess

        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="LICENSE.txt",
    url=URL,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    install_requires=[
        "Django>=1.3",
    ],
    setup_requires=[
        "jsmin",
        "cssmin",
    ],
    zip_safe=False,
    cmdclass={'test': PyTest},
)
