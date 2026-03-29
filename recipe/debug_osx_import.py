#!/usr/bin/env python3
"""
Debug helper for import-time crashes (e.g. SIGSEGV) on macOS only.

Typical CI failure (faulthandler): crash while loading the *native* pybind module
for ``pyngcore`` (importlib create_module), after ``numpy`` already loaded.
``netgen`` then pulls in ``pyngcore`` — import ``pyngcore`` first to pin the step.

Next steps if it still segfaults on ``pyngcore``: check the ``.so`` with
``otool -L`` / ``install_name_tool`` (RPATH, libngcore, OCCT, Python).

Usage (on a Mac, in an env where netgen is installed):
  PYTHONFAULTHANDLER=1 python debug_osx_import.py

Or from recipe dir:
  PYTHONFAULTHANDLER=1 python recipe/debug_osx_import.py

On non-macOS, exits 0 immediately (no-op) so you can keep one command in docs/CI snippets.
"""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path


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

    def run_step(name: str, fn) -> None:
        print(f"--> import {name} ...", flush=True)
        try:
            fn()
        except BaseException as e:
            print(f"!!! failed on import {name}: {e!r}", file=sys.stderr, flush=True)
            raise
        print(f"    ok: {name}", flush=True)

    run_step("numpy", lambda: __import__("numpy"))

    # Before loading pyngcore's native extension: log paths for otool -L on a real machine
    spec = importlib.util.find_spec("pyngcore")
    print("pyngcore find_spec:", spec, flush=True)
    if spec and spec.submodule_search_locations:
        for loc in spec.submodule_search_locations:
            d = Path(loc)
            print("  pyngcore package dir:", d, flush=True)
            if d.is_dir():
                for p in sorted(d.iterdir()):
                    print("   ", p.name, flush=True)

    # Crash is here: importlib create_module for the pybind .so (see faulthandler).
    run_step("pyngcore", lambda: __import__("pyngcore"))
    run_step("netgen", lambda: __import__("netgen"))

    print("--- all imports succeeded ---", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
