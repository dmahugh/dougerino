"""Setup program for dougerino
"""
from setuptools import setup

setup(
    name='Dougerino',
    version='1.0',
    license='MIT License',
    author='Doug Mahugh',
    py_modules=['dougerino'],
    install_requires=[
        'azure>=1.0.3',
        'azure-common>=1.1.4',
        'azure-datalake-store>=0.0.5',
        'azure-mgmt-datalake-store>=0.1.3',
        'requests>=2.12.3'
    ]
)