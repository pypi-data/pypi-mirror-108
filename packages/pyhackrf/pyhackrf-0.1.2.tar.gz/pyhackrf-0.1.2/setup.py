# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hackrf']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.3,<2.0.0']

setup_kwargs = {
    'name': 'pyhackrf',
    'version': '0.1.2',
    'description': 'Python wrapper for the libhackrf library',
    'long_description': "# pyhackrf\n\n## Motivation\n\nAll python bindings for hackrf are experimental at best and the installation is quite quirky and weird.\nThis is an attempt to change that.\n\n## Installation\n\n```\npip install pyhackrf\n```\n\n## Quick Example\n\nTo take samples and plot the power spectral density:\n\n```python\nfrom hackrf import *\nfrom pylab import *     # for plotting\n\nwith HackRF() as hrf:\n\thrf.sample_rate = 20e6\n\thrf.center_freq = 88.5e6\n\n\tsamples = hackrf.read_samples(2e6)\n\n\t# use matplotlib to estimate and plot the PSD\n\tpsd(samples, NFFT=1024, Fs=hackrf.sample_rate/1e6, Fc=hackrf.center_freq/1e6)\n\txlabel('Frequency (MHz)')\n\tylabel('Relative power (dB)')\n\tshow()\n```\n\n# More Example Use\n\nTo create a hackrf device:\n\n```python\nfrom hackrf import *\n\nhrf = HackRF()\n```\n\nIf you have two HackRFs plugged in, you can open them with the `device_index` argument:\n\n```python\nhackrf1 = HackRF(device_index = 0)\nhackrf2 = HackRF(device_index = 1)\n```\n\n### Callbacks\n\n```python\ndef my_callback(hackrf_transfer):\n    c = hackrf_transfer.contents\n    values = cast(c.buffer, POINTER(c_byte*c.buffer_length)).contents\n    iq = bytes2iq(bytearray(values))\n\n    return 0\n\n\n# Start receiving...\nhackrf.start_rx(my_callback)\n\n# If you want to stop receiving...\nhackrf.stop_rx()\n```\n\n### Gains\n\nThere is a 14 dB amplifier at the front of the HackRF that you can turn on or off.\nThe default is off.\n\nThe LNA gain setting applies to the IF signal.\nIt can take values from 0 to 40 dB in 8 dB steps.\nThe default value is 16 dB.\n\nThe VGA gain setting applies to the baseband signal.\nIt can take values from 0 to 62 dB in 2 dB steps.\nThe default value is 16 dB.\n\nThe LNA and VGA gains are set to the nearest step below the desired value.\nSo if you try to set the LNA gain to 17-23 dB, the gain will be set to 16 dB.\nThe same applies for the VGA gain; trying to set the gain to 27 dB will result in 26 dB.\n\n```python\n# enable/disable the built-in amplifier:\nhackrf.enable_amp()\nhackrf.disable_amp()\n\n# setting the LNA or VGA gains\nhackrf.lna_gain = 8\nhackrf.vga_gain = 22\n\n# can also use setters or getters\nhackrf.set_lna_gain(8)\nhackrf.set_vga_gain(22)\n```\n\n## Acknowledgements\n\nFor now most of the work is based on [this](https://github.com/dressel/pyhackrf).\nThat is going to change, also this notice will be removed then.\n\n## License\n\nThis project is licensed under the GPL-3 license.\n",
    'author': '4thel00z',
    'author_email': '4thel00z@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
