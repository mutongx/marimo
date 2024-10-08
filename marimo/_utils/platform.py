# Copyright 2024 Marimo. All rights reserved.
from __future__ import annotations

import sys


def is_windows() -> bool:
    return sys.platform == "win32" or sys.platform == "cygwin"


def is_pyodide() -> bool:
    return "pyodide" in sys.modules
