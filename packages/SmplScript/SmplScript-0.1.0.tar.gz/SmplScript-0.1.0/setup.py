from setuptools import setup

def readme():
    with open('README.md', 'r') as f:
        README = f.read()
    return README

setup(
    name='SmplScript',
    version='0.1.0',
    description='A language written from python, meant for beginners',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/CubesandSLEIGHTS/SmplScript',
    author='Stephen Steyaert',
    author_email='stephen.a.steyaert@gmail.com',
    license='GNU General Public v2',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['SmplScript'],
    include_package_data=True,
    install_requires=['termcolor'],
    entry_points={'console__scripts': [
        "SmplScript=SmplScript.run:run_language",
        ]
    }
)