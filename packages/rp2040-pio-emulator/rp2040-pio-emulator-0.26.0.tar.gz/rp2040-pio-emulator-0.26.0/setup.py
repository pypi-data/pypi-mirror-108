# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pioemu', 'pioemu.instructions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rp2040-pio-emulator',
    'version': '0.26.0',
    'description': 'RP2040 emulator for the testing and debugging of PIO programs',
    'long_description': '# Emulator for the PIO Blocks within the RP2040 Microcontroller (Python Edition)\n\n![Build Status](https://github.com/NathanY3G/rp2040-pio-emulator/actions/workflows/package-ci.yml/badge.svg) ![Coverage](./docs/images/coverage-badge.svg) [![PyPI](https://img.shields.io/pypi/v/rp2040-pio-emulator?color=informational)](https://pypi.org/project/rp2040-pio-emulator/)\n\n## Introduction\nAn emulator for the Programmable Input/Output (PIO) blocks that are present\nwithin the Raspberry Pi Foundation\'s RP2040 Microcontroller. It is designed\nto assist in the analysis of PIO programs and to help you by:\n\n* Enabling unit tests to be written.\n* Answering questions such as: How many clock cycles are being consumed?\n* Supporting the visualization of GPIO outputs over time.\n* Providing alternatives to debugging on real hardware, which can be time consuming.\n\n## Quick Start\nBelow is a slight variation of the example used within the [Quick Start Guide](./docs/Quick%20Start%20Guide.md).\n\n```python\nfrom pioemu import emulate\n\nprogram = [0xE029, 0x0041, 0x2080]  # Count down from 9 using X register\n\ngenerator = emulate(program, stop_when=lambda _, state: state.x_register < 0)\n\nfor before, after in generator:\n  print(f"X register: {before.x_register} -> {after.x_register}")\n```\n\n## Additional Examples\nSome additional examples include:\n\n1. Visualisation of square wave program using Jupyter Notebooks within the `examples/` directory.\n\n![Screenshot of square-wave program in Jupyter Notebooks](./examples/jupyter-notebook/jupyter_example.png)\n\n2. Example for the Pimoroni Blinkt! with Unit Test within the `examples/` directory.\n3. [pico-pio-examples](https://github.com/NathanY3G/pico-pio-examples)\n\n## Limitations\nThis software is under development and currently has limitations - the notable ones are:\n\n1. Only supports a sub-set of the available instructions:\n\n   * JMP (PIN and !OSRE variants not implemented)\n   * MOV (some variants and operations not implemented)\n   * OUT (PC, ISR and EXEC destinations not implemented)\n   * PULL (IfEmpty not implemented)\n   * SET\n   * WAIT (IRQ variant not implemented)\n\n1. No support for OUT, SET or IN pin-sets; all pin numbers are with respect to Pin 0.\n\n1. Pin-sets do not wrap after GPIO 31.\n\n1. No direct support for the concurrent running of multiple PIO programs;\n   a single State Machine is emulated and not an entire PIO block.\n',
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
