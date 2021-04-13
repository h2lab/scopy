# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import os.path

readme = ''
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.md')
if os.path.exists(readme_path):
    with open(readme_path, 'rb') as stream:
        readme = stream.read().decode('utf8')


setup(
    long_description=readme,
    name='scopy',
    version='0.0.1',
    description='Generic Python Scope Controller',
    python_requires='==3.*,>=3.7.0',
    project_urls={"documentation": "TODO", "homepage": "TODO", "repository": "TODO"},
    author='Mathieu RENARD',
    author_email='mathieu.renard@gotohack.org',
    license='LGPL-2.1+',
    packages=['scopy', 'scopy._ifaces','scopy.scopes'],
    package_dir={"": ".", "_ifaces": "./ifaces", "scopes":"./scopes"},
    package_data={},
    install_requires=['numpy>=1.19.1','matplotlib>=3.0.3'],
    extras_require={},
    entry_points={
        'console_scripts': [
            'scopy = scopy.__main__:script',
        ]
    },
)
