"""Sphinx configuration."""

project = "CheckedID Python API client"
author = "Jelmer Draaijer"
copyright = "2022, Jelmer Draaijer"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
