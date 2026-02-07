#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cobol backend server which adds a CobolAnalyserProvider and a
DocumentWordsProvider to the CodeCompletion worker.
"""
import os
import sys


def _add_sys_path(p: str) -> None:
    if p and os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)


def _add_extlibs_candidates() -> None:
    # 1) Prefer environment override if provided
    _add_sys_path(os.environ.get("OCIDE_EXTLIBS_PATH", "").strip())

    # 2) extlibs next to this script (some layouts)
    here = os.path.abspath(os.path.dirname(__file__))
    _add_sys_path(os.path.join(here, "extlibs"))

    # 3) OpenCobolIDE installed package layout (Slackware)
    _add_sys_path("/usr/lib64/python3.9/site-packages/open_cobol_ide/extlibs")

    # 4) If extlibs already points at ".../extlibs", also allow ".../extlibs/pyqode"
    # (not strictly necessary, but harmless)
    for p in list(sys.path)[:10]:
        if p.endswith(os.sep + "extlibs"):
            _add_sys_path(os.path.join(p, "pyqode"))


_add_extlibs_candidates()


if __name__ == "__main__":
    from pyqode.core import backend
    from pyqode.cobol.backend.workers import CobolCodeCompletionProvider

    backend.CodeCompletionWorker.providers.append(CobolCodeCompletionProvider())
    backend.DocumentWordsProvider.separators.remove("-")
    backend.CodeCompletionWorker.providers.append(backend.DocumentWordsProvider())
    backend.serve_forever()
