# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_explorer',
 'django_explorer.templatetags',
 'django_explorer.templatetags.themes']

package_data = \
{'': ['*'], 'django_explorer': ['templates/django_explorer/*']}

install_requires = \
['django>=3,<4', 'pydantic>=1.8.2,<2.0.0', 'python-magic>=0.4.22,<0.5.0']

extras_require = \
{':python_version >= "3.7"': ['ipython>=7.0.0,<8.0.0']}

setup_kwargs = {
    'name': 'django-explorer',
    'version': '0.3.0',
    'description': 'Serve local direcotry listing from django',
    'long_description': '# django_explorer\n\nServe local direcotry listing from your django app\n\n## Demo app\n\n1. Install dependencies `poetry install`\n2. Run demo app `make run_demo_app` (`make run_demo_app port=8888` if you want to use custom port)\n\n## Themes\n\n### Plain\n\n`http://localhost:8000/`\n![image](https://user-images.githubusercontent.com/18076967/120086128-1c9d1600-c0e6-11eb-8535-2948179829a5.png)\n`http://localhost:8000/nested_dir`\n![image](https://user-images.githubusercontent.com/18076967/120086149-30e11300-c0e6-11eb-9a31-dbbd4b1155a1.png)\n`http://localhost:8000/lorem_ipsum.md`\n![image](https://user-images.githubusercontent.com/18076967/120086173-5837e000-c0e6-11eb-9176-ffc2df59a0ff.png)\n',
    'author': 'dhvcc',
    'author_email': '1337kwiz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dhvcc/django_explorer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
