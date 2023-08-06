from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='gdbundbrm',
    version='1.1.0',
    url='',
    license='MIT License',
    author='Grupo Dom Bosco',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='nti@undb.edu.br',
    keywords='RM',
    description=u'integração API RM',
    packages=['gdbundbrm'],
    install_requires=['requests','djangorestframework'],)