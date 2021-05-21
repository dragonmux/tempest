# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import sphinx_rtd_theme


# -- Project information -----------------------------------------------------

project = 'Tempest'
copyright = '2021, Tempest Contributors'
author = 'Tempest Contributors'


# -- General configuration ---------------------------------------------------
extensions = [
	'sphinx.ext.githubpages',
	'sphinx.ext.graphviz',
	'sphinx.ext.autosectionlabel',
	'sphinx_rtd_theme',
	'myst_parser',
]

templates_path = [
	'./_templates'
]

source_suffix = {
	'.md': 'markdown',
}

exclude_patterns = [
	'.venv/*',
	'config.py',
	'LICENSE',
]

graphviz_output_format = 'svg'

html_theme = 'sphinx_rtd_theme'
# html_sidebars = { '**': ['about.html', 'relations.html', 'navigation.html'] }

autosectionlabel_prefix_document = True
