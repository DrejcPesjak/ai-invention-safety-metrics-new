"""Alias shim: the vendored iteration-2 module imports its siblings by their
original names. Re-exporting here keeps vendored_*.py BYTE-IDENTICAL to the
source (their sha256 is recorded in method_out.json) with zero patches.
"""
from vendored_lib_metrics import *  # noqa: F401,F403
import vendored_lib_metrics as _m
import sys as _sys
_sys.modules[__name__].__dict__.update(
    {k: v for k, v in _m.__dict__.items() if not k.startswith("__")})
