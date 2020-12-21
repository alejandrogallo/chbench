#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages


def get_version(filename):
    """Extract the package version"""
    with open(filename) as in_fh:
        for line in in_fh:
            if line.startswith('__version__'):
                return line.split('=')[1].strip()[1:-1]
    raise ValueError("Cannot extract version from %s" % filename)


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'numpy',
    'matplotlib',
    'ase',
]

dev_requirements = [
    'coverage', 'pytest', 'pytest-cov',
    'flake8']
dev_requirements.append('better-apidoc')


version = get_version('./src/chbench/__init__.py')

setup(
    author="Alejandro Gallo",
    author_email='aamsgallo@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Chemistry Bench",
    # entry_points=dict(
        # console_scripts=[
            # 'chbench=chbench:main'
        # ]
    # ),
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
    },
    license="GNU General Public License v3",
    long_description=readme,
    include_package_data=True,
    keywords='chbench',
    name='chbench',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url='https://github.com/alejandrogallo/chbench',
    version=version,
    zip_safe=False,
)
