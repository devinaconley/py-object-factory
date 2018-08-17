import setuptools

with open( 'README.md', 'r' ) as fh:
    long_description = fh.read()

setuptools.setup(
    name='objectfactory',
    version='0.0.1',
    author='Devin A. Conley',
    author_email='devinaconley@gmail.com',
    description='A python package for the serializable model / factory pattern',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/devinaconley/py-object-factory',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
