# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['olas']

package_data = \
{'': ['*']}

install_requires = \
['Cartopy>=0.18.0,<0.19.0',
 'dask[complete]>=2021.3.0,<2022.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'netCDF4>=1.5.6,<2.0.0',
 'numpy>=1.20.1,<2.0.0',
 'scipy>=1.6.1,<2.0.0',
 'xarray>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'olas',
    'version': '0.1.7',
    'description': 'Library with wave tools like ESTELA',
    'long_description': '# olas\n\n[![pypi package\nversion](https://img.shields.io/pypi/v/olas.svg)](https://pypi.python.org/pypi/olas)\n[![conda-forge\nversion](https://img.shields.io/conda/vn/conda-forge/olas.svg)](https://anaconda.org/conda-forge/olas)\n[![python supported\nshield](https://img.shields.io/pypi/pyversions/olas.svg)](https://pypi.python.org/pypi/olas)\n\nLibrary with wave tools. At the moment it only includes a prototype of ESTELA.\n\nDocumentation: <https://jorgeperezg.github.io/olas>\n\nThe documentation is generated with `poetry run portray on_github_pages`\n\n## Installation\n\nInstallation with conda is straightforward\n```\nconda install -c conda-forge olas\n```\n\nInstallation with pip requires cartopy (it can be installed with `conda install -c conda-forge cartopy`):\n```\npip install olas\n```\n\n## Basic usage\nCalculate and plot ESTELA maps from netcdf files.\n\n```\nfrom olas.estela import calc, plot\nestelas = calc("./tests/sample_files/test20180101T??.nc", 44, -4, "hs", "tp", "dp")\nplot(estelas, outdir=".")\nplot(estelas, gainloss=True, outdir=".")\n```\n',
    'author': 'jorge.perez',
    'author_email': 'j.perez@metocean.co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jorgeperezg/olas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
