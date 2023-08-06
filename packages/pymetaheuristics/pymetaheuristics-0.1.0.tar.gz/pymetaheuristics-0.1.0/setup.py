# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymetaheuristics',
 'pymetaheuristics.genetic_algorithm',
 'pymetaheuristics.genetic_algorithm.steps',
 'pymetaheuristics.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymetaheuristics',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Pymetaheuristics\n\nCombinatorial Optimization problems with quickly good soving.\n\n[![Continuous Integration](https://github.com/igormcsouza/pymetaheuristics/actions/workflows/integration.yml/badge.svg)](https://github.com/igormcsouza/pymetaheuristics/actions/workflows/integration.yml)\n[![Coverage Status](https://coveralls.io/repos/github/igormcsouza/pymetaheuristics/badge.svg?branch=master)](https://coveralls.io/github/igormcsouza/pymetaheuristics?branch=master)\n\n\n## Introduction\n\nPymetaheuristics is a package to help build and train Metaheuristics to solve\nreal world problems mathematically modeled. It strives to generalize the\noverall idea of the technic and delivers to the user a friendly wrapper so the\ncientist may focus on the problem modeling rather than the heuristic\nimplementation. This package is an open source project so feel free to send\nyour implementations and fixes so they may be helpful for others too.\n\n\n## Subpackages\n\nThe idea is to implement all possible Metaheuristics found on the market today\nand some helper functions to improve what is already there.\n**Note: This package is under construction, new features will come up soon.**\n\nWhat Metaheuristics can be found on this project?\n\n1. Genetic Algorithm\n\n## How to use\n\nFirst install the package (available on pypi)\n```bash\n$ pip install pymetaheuristics\n```\n\nImport the algorithm model you want to use to solve you problem. Implement the\nneeded functions and pass to the model. Train and get the results.\n```python\nfrom pymetaheuristics.genetic_algorithm.model import GeneticAlgorithm\n\nmodel = GeneticAlgorithm(\n    fitness_function=fitness_function,\n    genome_generator=genome_generator\n)\n\nresult = model.train(\n    epochs=15, pop_size=10, crossover=pmx_single_point, verbose=True)\n```\n\nEvery module has its integration test, which I submit the model for testing\nwith very know NP-Hard problems today (Knapsack, tsp, ...). If you want to see\nhow it goes, check out the integrations under the model testing folder.\n\n## How to contribute\n\nYour code and help is very appreciate! Please, send your issue and pr's \nwhenever is good for you! If needed, send an \n[email](mailto:igormcsouza@gmail.com) to me I'll be very glad to help. Let's \nbuild up together.",
    'author': 'Igor Souza',
    'author_email': 'igormcsouza@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/igormcsouza/pymetaheuristics',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
