from common_conf import *

import os, sys, datetime

if not os.path.exists('../../dss-extensions'):
    raise RuntimeError('dss-extensions common repo not found. Be sure to clone it side-by-side with OpenDSSDirect.py when building docs.')

if not os.path.exists('../../dss_python_backend'):
    raise RuntimeError('dss_python_backend common repo not found. Be sure to clone it side-by-side with OpenDSSDirect.py when building docs.')

sys.path.append('../../dss-extensions/docs')
from common_conf import *
from opendssdirect import dss

project = 'DSS-Extensions'
copyright = '2018-2024 DSS-Extensions contributors'
author = 'DSS-Extensions contributors'
# version = datetime.date.isoformat().replace('-', '.')
# release = version
html_theme = "pydata_sphinx_theme"
html_theme_options = {}

exclude_patterns.append('python/enums.md')
exclude_patterns.append('dss-format/toc.md')
html_title = "DSS-Extensions"

# html_theme_options["navbar_start"] = ["navbar-logo", "navbar-nav"]
html_theme_options["navbar_start"] = ["navbar-logo"]
html_theme_options["navbar_center"] = ["navbar-nav"]
html_theme_options["logo"] = {
    "text": project,
}
# html_theme_options["home_page_in_toc"] = False
html_favicon = '../images/dssx.svg'
html_logo = '../images/dssx.svg'
# html_logo = '../images/dss-extensions-horizontal.svg'

html_sidebars = {
    "*": [],
    "docs": ["sidebar-nav-bs", ],
    "dss_language": ["sidebar-nav-bs", ],
    "dss-format/*": ["sidebar-nav-bs", ],
    "classic_api": ["sidebar-nav-bs", ],
    "python_apis": ["sidebar-nav-bs", ],
    "multithreading": ["sidebar-nav-bs", ],
}

html_static_path = ['_static']
html_css_files = [
    'custom.css',
]

html_theme_options["header_links_before_dropdown"] = 5

# html_theme_options["external_links"] = [
#     {"name": "AltDSS/DSS C-API", "url": "https://github.com/dss-extensions/dss_capi/"},
#     {"name": "DSS-Python", "url": "https://dss-extensions.org/DSS-Python/"},
#     {"name": "AltDSS-Python", "url": "https://dss-extensions.org/AltDSS-Python/"},
#     {"name": "OpenDSSDirect.py", "url": "https://dss-extensions.org/OpenDSSDirect.py/"},
#     {"name": "OpenDSSDirect.jl", "url": "https://dss-extensions.org/OpenDSSDirect.jl/"},
#     {"name": "DSS_Sharp", "url": "https://github.com/dss-extensions/dss_sharp"},
#     {"name": "DSS_MATLAB", "url": "https://github.com/dss-extensions/DSS_MATLAB"},
#     {"name": "AltDSS-Rust", "url": "https://github.com/dss-extensions/AltDSS-Rust"},
#     {"name": "AltDSS-Go", "url": "https://github.com/dss-extensions/AltDSS-Go"},
# ]


html_theme_options["icon_links"] = [{
    "name": "DSS-Extensions Org. on GitHub",
    "url": "https://github.com/dss-extensions/",
    "icon": "fa-brands fa-square-github",
    "type": "fontawesome",
}]

def setup(app):
    return {
        "parallel_write_safe": True,
        "parallel_read_safe": True,
    }

highlight_language = 'none'