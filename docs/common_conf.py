import re

extensions = [
    'sphinx.ext.intersphinx',
    'sphinxcontrib.mermaid',
    # 'sphinx.ext.coverage',
    # 'sphinx.ext.mathjax',
    # 'sphinx.ext.githubpages',
    #'nbsphinx',
    'myst_nb',
    #'myst_parser',
    'sphinx_design',
]

templates_path = ['_templates']
source_suffix = ['.md']
language = 'en'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints', 'docs/README.md', '**.virtual_documents']
html_theme = "sphinx_book_theme"
html_theme_options = {
    "footer_content_items": ["copyright", "last-updated", "extra-footer"],
    "navigation_with_keys": False,
#   "footer_center": ["copyright", ],
#   "footer_start": [],
#   "footer_end": [],
}

autodoc2_render_plugin = "myst"
autodoc2_hidden_objects = ['private']

myst_heading_anchors = 3
myst_linkify_fuzzy_links = False
myst_fence_as_directive = ["mermaid"]
nb_execution_allow_errors = True
nb_number_source_lines = False

linkcheck_ignore = [
    re.escape('https://opendss.epri.com/') + '.*',
]

myst_enable_extensions = [
    "smartquotes",
    "linkify",
    "attrs_inline",
    "colon_fence",
    "dollarmath",
    "fieldlist",
    "strikethrough",
    "attrs_block",

    # "amsmath",
    # "deflist",
    # "html_admonition",
    # "html_image",
    # "replacements",
    # "tasklist",
]


def patch_autodoc2():
    # Monkey-patch autodoc2
    from astroid import nodes
    import autodoc2.astroid_utils

    get_const_values_org = autodoc2.astroid_utils.get_const_values

    def get_const_values(node):
        try:
            return get_const_values_org(node)
        except:
            if isinstance(node, nodes.Call):
                return None
        
            raise

    autodoc2.astroid_utils.get_const_values = get_const_values
