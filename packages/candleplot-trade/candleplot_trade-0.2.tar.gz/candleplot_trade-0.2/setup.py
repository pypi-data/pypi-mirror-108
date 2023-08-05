from setuptools import setup
requirements = ["requests<=2.21.0"]

setup(name='candleplot_trade',
      version='0.2',
      description='online trading based on indicators and candles',
      packages=['candleplot_trade'],
      author_email='info@zungl.ru',
      install_requires=requirements,
      zip_safe=False)
