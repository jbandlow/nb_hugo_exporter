r"""Simple setup.py file.

TODO: Bump version, add classifiers. Possibly add a script.
"""

import setuptools

with open("README.md") as readme:
    long_description = readme.read()

setuptools.setup(
    name='nbhugoexporter',
    version='0.1dev',
    author='Jason Bandlow',
    author_email='jbandlow@gmail.com',
    description='Export Jupyter notebooks to a Hugo compatible format',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jbandlow/nb_hugo_exporter',
    packages=setuptools.find_packages(),
    install_requires=['nbconvert', 'traitlets'],
    entry_points={
        'nbconvert.exporters': [
            'hugo = nbhugoexporter.hugoexporter:HugoExporter',
        ],
    },
    include_package_data=True,
)
