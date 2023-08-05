# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pioemu', 'pioemu.instructions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rp2040-pio-emulator',
    'version': '0.21.0',
    'description': 'RP2040 emulator for the testing and debugging of PIO programs',
    'long_description': "# Emulator for the PIO Blocks within the RP2040 Microcontroller (Python Edition)\n\n![Build Status](https://github.com/NathanY3G/rp2040-pio-emulator/actions/workflows/package-ci.yml/badge.svg) ![Coverage](./docs/images/coverage-badge.svg) [![PyPI](https://img.shields.io/pypi/v/rp2040-pio-emulator?color=informational)](https://pypi.org/project/rp2040-pio-emulator/)\n\n## Introduction\npioemu is an emulator for the Programmable Input/Output (PIO) blocks that are\npresent within the Raspberry Pi Foundation's RP2040 Microcontroller. It is\ndesigned to assist in the analysis of PIO programs and to help you by:\n\n* Enabling unit tests to be written.\n* Answering questions such as: How many clock cycles are being consumed?\n* Supporting the visualization of GPIO outputs over time.\n* Providing alternatives to debugging on real hardware, which can be time consuming.\n\n## Examples\n\n### Pimoroni Blinkt! with Unit Test\nAn annotated example which demonstrates one approach to writing unit tests for\nPIO programs by using an emulator. The PIO program itself is very primitive and\nsets all eight LEDs of a Pimoroni Blink! to a single hard-coded colour. Perhaps\nyou would to like to try re-factoring it? Don't forget to check that the unit-test\nstill passes!\n\n### Jupyter Notebook\nThe emulator can also be used from within Jupyter Notebooks. The screenshot below\nis taken from the ``examples/jupyter-notebook/square_wave_example.ipynb`` notebook\nthat is included within this repository.\n\n![Screenshot of Jupyter Notebook example](./docs/images/jupyter_example.png)\n\n### Limitations\nThis software is under development and currently has limitations - the notable ones are:\n\n1. Only supports a sub-set of the available instructions:\n\n   * JMP (PIN and !OSRE variants not implemented)\n   * MOV (some variants and operations not implemented)\n   * OUT (PC, ISR and EXEC destinations not implemented)\n   * PULL (IfEmpty not implemented)\n   * SET\n   * WAIT (IRQ variant not implemented)\n\n1. No support for OUT, SET or IN pin-sets; all pin numbers are with respect to Pin 0.\n\n1. Pin-sets do not wrap after GPIO 31.\n\n1. No direct support for the concurrent running of multiple PIO programs;\n   a single State Machine is emulated and not an entire PIO block.\n",
    'author': 'Nathan Young',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NathanY3G/rp2040-pio-emulator',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
