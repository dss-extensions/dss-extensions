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
# html_theme = "pydata_sphinx_theme"
# del html_theme_options

exclude_patterns.append('python/enums.md')

html_theme_options["navbar_start"] = ["navbar-logo"]