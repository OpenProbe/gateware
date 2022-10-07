# -*- coding: utf-8 -*-
#
# This file is part of OpenProbe
#

from setuptools import setup

packages = [
    "applet",
    "board",
    "soc",
    "soc.zynq",
]

package_data = {"": ["*"]}

requirements = [
    "amaranth"
]

setup_kwargs = {
    "name": "OpenProbe",
    "description": "Amaranth HDL framework for OpenProbe project",
    "long_description": None,
    "author": "OpenProbe Community",
    "author_email": None,
    "maintainer": None,
    "url": None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': requirements,
    'python_requires': '>=3.7,<4.0',
}

setup(**setup_kwargs)
