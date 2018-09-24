
from setuptools import setup

setup_args = dict (
    name="rsplib",
    version="0.9",
    description= 'A Python Client for RSP',
    license='MIT',
    url='https://github.com/riccardotommasini/colorwave',
    author='RSP Gang',
    author_email='riccardo.tommasini@polimi.it',
    packages=[ "rsplib" ],
    install_requires = [ 'setuptools',
                         'pandas',
                         'json2html',
                         'requests',
                         'matplotlib',
                         'pygments',
                         'websocket-client',
                         'rdflib',
                         'rdflib-jsonld',
                         'json2html',
                         'pydot' ])


if __name__ == '__main__':
    setup( **setup_args )