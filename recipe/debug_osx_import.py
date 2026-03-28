#!/usr/bin/env python3
"""
Debug helper for import-time crashes (e.g. SIGSEGV) on macOS only.

Usage (on a Mac, in an env where netgen is installed):
  PYTHONFAULTHANDLER=1 python debug_osx_import.py

Or from recipe dir:
  PYTHONFAULTHANDLER=1 python recipe/debug_osx_import.py

On non-macOS, exits 0 immediately (no-op) so you can keep one command in docs/CI snippets.
"""
from __future__ import annotations

import os
import sys


def _is_osx() -> bool:
    return sys.platform == "darwin"


def main() -> int:
    if not _is_osx():
        print("debug_osx_import.py: skipped (not macOS / darwin).", file=sys.stderr)
        return 0

    # Optional: reduce BLAS/thread noise when isolating segfaults
    for k, v in (
        ("OMP_NUM_THREADS", "1"),
        ("OPENBLAS_NUM_THREADS", "1"),
        ("MKL_NUM_THREADS", "1"),
        ("VECLIB_MAXIMUM_THREADS", "1"),
        ("NUMEXPR_NUM_THREADS", "1"),
    ):
        os.environ.setdefault(k, v)

    try:
        import faulthandler

        faulthandler.enable(all_threads=True)
    except Exception as e:
        print(f"faulthandler.enable failed: {e}", file=sys.stderr)

    print("--- debug_osx_import (macOS) ---", flush=True)
    print("executable:", sys.executable, flush=True)
    print("version:", sys.version.replace("\n", " "), flush=True)

    steps = [
        ("numpy", lambda: __import__("numpy")),
        ("netgen", lambda: __import__("netgen")),
    ]

    for name, fn in steps:
        print(f"--> import {name} ...", flush=True)
        try:
            fn()
        except BaseException as e:
            print(f"!!! failed on import {name}: {e!r}", file=sys.stderr, flush=True)
            raise
        print(f"    ok: {name}", flush=True)

    print("--- all imports succeeded ---", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
