#!/usr/bin/env python3
"""
Debug helper for import-time crashes (e.g. SIGSEGV) on macOS only.

Typical CI failure (faulthandler): crash while loading the *native* pybind module
for ``pyngcore`` (importlib create_module), after ``numpy`` already loaded.
``netgen`` then pulls in ``pyngcore`` — import ``pyngcore`` first to pin the step.

The script runs ``otool -L`` on ``pyngcore``'s ``.so`` and on ``$PREFIX/lib/libngcore*.dylib``
before importing, so CI logs show linkage even when import crashes.
Further local checks: ``install_name_tool``, RPATH (``otool -l`` / ``grep LC_RPATH``).

Usage (on a Mac, in an env where netgen is installed):
  PYTHONFAULTHANDLER=1 python debug_osx_import.py

Or from recipe dir:
  PYTHONFAULTHANDLER=1 python recipe/debug_osx_import.py

On non-macOS, exits 0 immediately (no-op) so you can keep one command in docs/CI snippets.
"""
from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path


def _otool_l(path: Path) -> None:
    """Print ``otool -L`` for CI logs (dylib linkage before import can segfault)."""
    otool = shutil.which("otool")
    if not otool:
        print("otool: not in PATH, skipping", file=sys.stderr, flush=True)
        return
    if not path.is_file():
        print(f"otool -L: skip (not a file): {path}", file=sys.stderr, flush=True)
        return
    print(f"\n--- otool -L {path} ---", flush=True)
    r = subprocess.run(
        [otool, "-L", str(path)],
        capture_output=True,
        text=True,
        timeout=120,
    )
    sys.stdout.write(r.stdout)
    if r.stderr:
        sys.stderr.write(r.stderr)
    if r.returncode != 0:
        print(f"otool exited {r.returncode}", file=sys.stderr, flush=True)


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
                for ext in ("*.so", "*.dylib"):
                    for so in sorted(d.glob(ext)):
                        _otool_l(so)

    libdir = Path(sys.prefix) / "lib"
    if libdir.is_dir():
        for dy in sorted(libdir.glob("libngcore*.dylib")):
            _otool_l(dy)

    # Crash is here: importlib create_module for the pybind .so (see faulthandler).
    run_step("pyngcore", lambda: __import__("pyngcore"))
    run_step("netgen", lambda: __import__("netgen"))

    print("--- all imports succeeded ---", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
