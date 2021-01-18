# objectfactory configuration file for sphinx documentation builder

import os
import sys

sys.path.insert( 0, os.path.abspath( '../../objectfactory/' ) )

# project info
project = 'objectfactory'
copyright = '2018-2021, Devin A. Conley'
author = 'Devin A. Conley'
release = '0.1.0'

# config
extensions = [
    'sphinx.ext.autodoc',
    'sphinx_rtd_theme',
    'm2r2'
]
autoclass_content = 'both'
html_theme = 'sphinx_rtd_theme'
