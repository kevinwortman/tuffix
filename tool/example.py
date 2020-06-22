#!/usr/bin/env python3.8

import os, sys

_here = os.path.abspath(os.path.dirname(__file__))
encoding = "utf-8" if sys.version_info[0] < 3 else None

with open(os.path.join(_here, 'README.md'), encoding=encoding) as f:
    long_description = f.read()
