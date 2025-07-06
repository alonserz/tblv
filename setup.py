from setuptools import setup

setup(
    name='tblv',
    author='alonserz',
    maintainer='alonserz',
    version='0.3',
    description = "Simple TensorBoard Log Viewer",
    packages = ['tblv'],
    install_requires= [
        'blessed',
        'plotext',
        'protobuf==3.20.1',
    ],
    entry_points={
        'console_scripts': [
            'tblv = tblv.tblv:main',
        ]
    },
)
