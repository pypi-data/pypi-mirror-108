from setuptools import setup
requirements = ["requests"]

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='candleplot_trade',
      version='0.6',
      description='online trading based on indicators and candles',
      packages=['candleplot_trade'],
      author_email='info@zungl.ru',
      install_requires=requirements,
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
