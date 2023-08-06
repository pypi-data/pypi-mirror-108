# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meet_man']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.4,<6.0.0', 'PyQtWebEngine>=5.15.4,<6.0.0']

entry_points = \
{'console_scripts': ['meet = meet_man.main:main']}

setup_kwargs = {
    'name': 'meet-man',
    'version': '0.1.4',
    'description': 'Google Meet Client',
    'long_description': '# meet-man\n### `meetman` : A simple Google Meet Client \n\n[![Downloads](https://static.pepy.tech/personalized-badge/lolacli?period=total&units=abbreviation&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/meet-man)\n\n\n#### Dependencies\n+ `PyQt5`\n+ `PyQtWebEngine`\n\n \n### Built with\n+ `Python 3.8.5` \n\n![python](https://raw.githubusercontent.com/MikeCodesDotNET/ColoredBadges/master/svg/dev/languages/python.svg)\n\n\n## Installation\n\n#### Method 2\n\nIf you have python and pip installed in your computer, execute the following\n\n```bash\npip3 install meet-man\n```\n\n### Guide\n\n- Open the app by typing `meet`\n\n```\nmeet\n```\n\n## Developer Tools\n\n- [Python 3.8.5](https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tar.xz) \n\n![python](https://raw.githubusercontent.com/MikeCodesDotNET/ColoredBadges/master/svg/dev/languages/python.svg)\n\n- [Sublime Text 3](https://www.sublimetext.com/3)\n\n- [Visual Studio Code](https://code.visualstudio.com) \n\n![vscode](https://raw.githubusercontent.com/MikeCodesDotNET/ColoredBadges/master/svg/dev/tools/visualstudio_code.svg)\n\n- [Git](https://git-scm.com/) \n\n![git](https://raw.githubusercontent.com/klaasnicolaas/ColoredBadges/new-badges/svg/dev/tools/git.svg)\n\n- [Python Poetry](https://python-poetry.org/) for package management and publishing\n\n## Release Notes\n\n- **Current Release- 0.1.1**\n\n#### Developers\n- [Arghya Sarkar](https://github.com/arghyagod-coder)\n\n## License\n\nLicense © 2021-Present Arghya Sarkar\n\nThis repository is licensed under the MIT license. See [LICENSE](https://github.com/arghyagod-coder/lola/master/LICENSE) for details.\n\n## Special Notes\n\n- Contribution is appreciated! Visit the contribution guide in [Contribution Guide](CONTRIBUTING.md)\n- Thanks for seeing my project!',
    'author': 'Arghya Sarkar',
    'author_email': 'arghyasarkar.joker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arghyagod-coder/meet-man',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
