# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['image_converter']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python>=4.5.2,<5.0.0',
 'pytesseract>=0.3.7,<0.4.0',
 'rich>=10.2.2,<11.0.0',
 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'code-image-to-text',
    'version': '0.1.4',
    'description': 'Convert code image to text',
    'long_description': '# Code Image to Text Converter\n\nConvert code image into text.\n\nFor example, if you want to extract code from the image named `images/carbon.png`.\n![image](https://github.com/khuyentran1401/code_image_to_text/blob/master/images/carbon.png?raw=True)\n\nType:\n```bash\npython -m image_converter images/carbon.png .py\n```\nThis will convert the image to text like below and save the code to the file named `carbon.py`.\n\n```python\nclass DataLoader:\n\n\t def __init__(self, data_dir: str):\n\t\t self.data_dir = data_dir\n\n\t\t print("Instance is created")\n\t def __call__(self):\n\n\t\t print("Instance is called")\n\ndata_loader = DataLoader(\'my_data_dir\')\n\ndata_loader()\n\n```\n\n# Installation\n## Intall Tesseract\n* Linux\n```bash\nsudo apt-get update\nsudo apt-get install tesseract-ocr\nsudo apt-get install libtesseract-dev\n```\n\n* Windows\nInstall from [here](https://github.com/UB-Mannheim/tesseract/wiki)\n## Install code-image-to-text\n```bash\npip install code-image-to-text\n```\n\n\n\n',
    'author': 'khuyentran1401',
    'author_email': 'khuyentran1476@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/khuyentran1401/code_image_to_text',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
