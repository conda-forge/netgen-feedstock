#!/usr/bin/env bash
# macOS-only helper to debug segmentation faults during Python import (e.g. netgen).
# On Linux/Windows: exits 0 immediately (no-op).

set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "debug_osx_import.sh: skipped (not macOS)." >&2
  exit 0
fi

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONFAULTHANDLER="${PYTHONFAULTHANDLER:-1}"

# Optional: uncomment to test under lldb
# exec lldb -- "${PYTHON:-python}" -u "${HERE}/debug_osx_import.py"
exec "${PYTHON:-python}" -u "${HERE}/debug_osx_import.py"
