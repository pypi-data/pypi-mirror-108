from setuptools import setup

setup(name='parse_spmei',
      version='0.1',
      description='Parseing site spmei.ru',
      packages=['parse_spmei'],
      author_email='molseryuij@gmail.com',
      install_requires=['requests>=2.25.1', 'bs4==0.0.1'],
      zip_safe=False)

