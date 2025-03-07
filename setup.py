import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='objectfactory',
    version='0.2.0b1',
    author='Devin A. Conley',
    author_email='devinaconley@gmail.com',
    description='objectfactory is a python package to easily implement the factory design pattern for object creation, serialization, and polymorphism',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/devinaconley/py-object-factory',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
    install_requires=[
        'marshmallow>=3,<4',
    ]
)
