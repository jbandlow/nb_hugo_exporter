r"""Simple setup.py file."""

import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    author='Jason Bandlow',
    author_email='jbandlow@gmail.com',
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
    description='Export Jupyter notebooks to a Hugo compatible format',
    entry_points={
        'nbconvert.exporters': [
            'hugo = nbhugoexporter.hugoexporter:HugoExporter',
        ],
    },
    include_package_data=True,
    install_requires=['nbconvert', 'traitlets'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    name='nbhugoexporter',
    packages=setuptools.find_packages(),
    url='https://github.com/jbandlow/nb_hugo_exporter',
    version='0.1.3',
)
