# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matching_network']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'quantiphy>=2.13.0,<3.0.0']

entry_points = \
{'console_scripts': ['matching_network = matching_network.__main__:cli']}

setup_kwargs = {
    'name': 'matching-network',
    'version': '0.1.6',
    'description': 'Design lumped-parameters matching networks (L-sections)',
    'long_description': '# matching_network\nSolve L-section lumped parameters matching networks in a wink. (See [How to use](#how-to-use) section)<br><br>\n\n### Shunt-series config.\n![](https://raw.githubusercontent.com/urbanij/matching-network/master/aux/figures/shunt_series_configuration.png)\n\n\n### Series-shunt config.\n![](https://raw.githubusercontent.com/urbanij/matching-network/master/aux/figures/series_shunt_configuration.png)\n\n\n<!-- Index of Jupyter (IPython) Notebooks -->\n\n|Jupyter Notebooks                                                                                                                              |\n|-----------------------------------------------------------------------------------------------------------------------------------------------|\n|<a href="https://urbanij.github.io/projects/matching_networks/">L-section_matching_calculations</a> (Initial Jupyter notebook implementation)|\n|<a href="https://urbanij.github.io/projects/matching_networks/calc.html">Calculations</a> (Matlab pre-calculations)                                     |\n\n\n---\n\n\n[![Downloads](https://pepy.tech/badge/matching-network)](https://pepy.tech/project/matching-network)\n\n\nInstallation\n============\n\n```sh\npip install matching_network\n```\n\n\nHow to use\n=============\n\n### From the CLI\n```bash\nmatching_network --from 100 --to 20+43j --freq 13.56e6 # both impedances in Ω. \n```\n```\nFrom (100+0j) Ω to (20+43j) Ω\n\nnormalized starting impedance = (100+0j)Ω / (20+43j)Ω = 0.88928-1.912j\n\n#solutions: 4\n\nshunt-series\n    Shunt Inductor:\n    X = 50 Ω ⇔ B = -20 mS\n    L = 586.85 nH  (@ 13.56 MHz)\n    Series Inductor:\n    X = 3 Ω ⇔ B = -333.33 mS\n    L = 35.211 nH  (@ 13.56 MHz)\nshunt-series\n    Shunt Capacitor:\n    X = -50 Ω ⇔ B = 20 mS\n    C = 234.74 pF  (@ 13.56 MHz)\n    Series Inductor:\n    X = 83 Ω ⇔ B = -12.048 mS\n    L = 974.18 nH  (@ 13.56 MHz)\nseries-shunt\n    Series Inductor:\n    X = 35.285 Ω ⇔ B = -28.341 mS\n    L = 414.14 nH  (@ 13.56 MHz)\n    Shunt Inductor:\n    X = 62.571 Ω ⇔ B = -15.982 mS\n    L = 734.4 nH  (@ 13.56 MHz)\nseries-shunt\n    Series Capacitor:\n    X = -35.285 Ω ⇔ B = 28.341 mS\n    C = 332.64 pF  (@ 13.56 MHz)\n    Shunt Inductor:\n    X = 44.929 Ω ⇔ B = -22.257 mS\n    L = 527.33 nH  (@ 13.56 MHz)\n```\n\n```bash\nmatching_network --from "24.3+8.3j mS"  --to 1.1+9.3j # default in Ω unless specified, using `mS`.\n```\n\n\n### Inside Python\n\n```python\n>>> import matching_network as mn\n>>>\n>>> impedance_you_have         = 90 + 32j # Ω\n>>> impedance_you_want_to_have = 175      # Ω\n>>>\n>>> frequency                  = 900e6    # Hz\n>>>\n>>> mn.L_section_matching(impedance_you_have, impedance_you_want_to_have, frequency).match()\nFrom (90+32j) Ω to 175 Ω\n\nnormalized starting impedance = (90+32j)Ω/175Ω = 0.51429+0.18286j\n\n#solutions: 2\n\nseries-shunt\n    Series Inductor:\n    X = 55.464 Ω ⇔ B = -18.03 mS\n    L = 9.8082 nH  (@ 900 MHz)\n    Shunt Capacitor:\n    X = -180.07 Ω ⇔ B = 5.5533 mS\n    C = 982.04 fF  (@ 900 MHz)\n\nseries-shunt\n    Series Capacitor:\n    X = -119.46 Ω ⇔ B = 8.3707 mS\n    C = 1.4803 pF  (@ 900 MHz)\n    Shunt Inductor:\n    X = 180.07 Ω ⇔ B = -5.5533 mS\n    L = 31.844 nH  (@ 900 MHz)\n\n>>>\n```\n\n<div align="right" style="text-align:right"><i><a href="https://urbanij.github.io/">Francesco Urbani</a></i></div>',
    'author': 'Francesco Urbani',
    'author_email': 'francescourbanidue@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/matching-network/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
