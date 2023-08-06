from os import path

from setuptools import setup, find_packages

import linum

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md")) as f:
    long_description = f.read()

setup(
    name='Linum',
    version=linum.__version__,
    packages=find_packages(exclude=["tests", "examples"]),
    package_data={"": ["*.yaml"]},
    url='https://github.com/chabErch/Linum',
    license='MIT',
    author='chaberch',
    author_email='chaberch@yandex.ru',
    description='The tool for tasks visualization — like Gantt chart, but compact.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent'
    ],
    keywords=[
        'Gantt', 'chart', 'schedule',
        'Linum',
        'render', 'visualisation',
        'excel', 'xlsx'
    ],
    entry_points={
        'console_scripts': [
            'linum = linum.cli:cli',
        ],
    }
)
