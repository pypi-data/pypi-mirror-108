from setuptools import setup, find_packages
from customtransformers import __version__

requirements = []
with open('requirements.txt', 'r') as reqs:
    requirements = reqs.read().split()

setup(
    name='customtransformers',
    version=__version__,
    description='A python library for custom transformers adapted to scikit-learn Pipeline / Transformers format',
    author='l4rakr0ft',
    author_email='l4rakr0ft@gmail.com',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3',
)
