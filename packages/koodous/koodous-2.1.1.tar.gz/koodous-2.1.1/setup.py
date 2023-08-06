#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = [ ]

setup(
    author="Rubén García Rojas",
    author_email='rgarcia@hispasec.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="This is the Python SDK developed by our team to use Koodous easily.",
    entry_points={
        'console_scripts': [
            'koodous=koodous.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='koodous',
    name='koodous',
    packages=find_packages(include=['koodous', 'koodous.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/koodous/python-sdk',
    version='2.1.1',
    zip_safe=False,
)
