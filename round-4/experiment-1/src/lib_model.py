"""Alias shim: the vendored iteration-3 module imports its siblings by their
original names. Re-exporting here keeps vendored_*.py BYTE-IDENTICAL to the
source (sha256 recorded in method_out.json) with zero patches."""
from vendored_lib_model import *  # noqa: F401,F403
import vendored_lib_model as _m
import sys as _sys
_sys.modules[__name__].__dict__.update(
    {k: v for k, v in _m.__dict__.items() if not k.startswith("__")})
