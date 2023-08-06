# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['termitext']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'termitext',
    'version': '0.1.7',
    'description': 'Color and format text in the console',
    'long_description': '# TermiText\n\n[Github page](https://github.com/Yekc/TermiText)\n\nColor and format text you print in the terminal!\nHere is an example on how to use TermiText:\n```python\nfrom termitext import *\n\n#Print green text with orange highlight\nprint(color("Hello world!", color = "green", highlight = "orange"))\n\n#Print on the same line\nslprint("This text is all ")\nslprint(" on the same line!")\n\n#Print bold text\nprint(format("Hello world!", style = "bold"))\n\n#Clear the terminal\nclear()\n```  \n**LIST OF COLORS:**  \n*Text: *lightred, red, orange, yellow, lightgreen, green, lightcyan, cyan, lightblue, blue, pink, purple, black, darkgrey, lightgrey\n*Highlight: *red, orange, green, cyan, blue, purple, black, lightgrey  \n\n**LIST OF FORMATS:**  \nbold, underline, strikethrough, invisible, reverse, disable  \n\n',
    'author': 'Yek',
    'author_email': 'gwojtysiak34@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
