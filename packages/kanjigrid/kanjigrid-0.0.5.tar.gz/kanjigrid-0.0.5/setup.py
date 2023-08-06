# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kanjigrid']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0']

entry_points = \
{'console_scripts': ['greet = kanjigrid.kanjigrid:greet']}

setup_kwargs = {
    'name': 'kanjigrid',
    'version': '0.0.5',
    'description': 'Create Kanji Grids out of Text',
    'long_description': '# kanjigrid\nCreate Kanji Grids out of Text\n\n```python\npip install kanjigrid\n```\n\n##  MWE\n```python\nimport kanjigrid\n\ngridder = kanjigrid.Gridder("Kanji", 40, "Header", 52)\ngrading = kanjigrid.Jouyou()\n\nwith open("test.txt", "r", encoding="utf-8") as f:\n    data = f.read()\n\ngridder.feed_text(data)\ngrid = gridder.make_grid(grading, outside_of_grading=True, stats=True, bar_graph=True)\ngrid.save("test.png")\n```\n\n![](https://github.com/exc4l/kanjigrid/blob/main/test.png)\n',
    'author': 'exc4l',
    'author_email': 'cps0537@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/exc4l/kanjigrid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
