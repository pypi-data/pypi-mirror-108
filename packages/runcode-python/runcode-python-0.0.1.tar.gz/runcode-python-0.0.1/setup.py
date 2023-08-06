import io
import os
from setuptools import setup, find_packages

VERSION = '0.0.1'
long_description_text = """runcode-python

"""

setup(
    name='runcode-python',
    version=VERSION,
    author='Micro Pyramid Informatic Pvt. Ltd.',
    author_email='hello@micropyramid.com',
    url='https://github.com/MicroPyramid/runcode-python',
    description='runcode-python.',
    long_description=long_description_text,
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    install_requires=[
        'simplejson',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Internationalization',
    ],
)
