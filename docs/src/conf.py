# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys, os, datetime
import django

sys.path.append(os.path.abspath("./"))
sys.path.append(os.path.abspath("../"))
sys.path.append(os.path.abspath("../../"))

os.environ["DJANGO_SETTINGS_MODULE"] = "docs_settings"
django.setup()

import swingtime
release = ".".join(str(i) for i in swingtime.VERSION)
version = ".".join(str(i) for i in swingtime.VERSION[:2])
project = 'Swingtime'
copyright = '{}, David Krauth'.format(datetime.date.today().year)
author = 'David Krauth'
extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode", "sphinx.ext.autosummary"]
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'sphinx_rtd_theme'
html_static_path = []
autosummary_generate = True

