OpenCobolIDE-4.7.7
------------------

OpenCobolIDE is no longer maintained, see https://github.com/OpenCobolIDE/OpenCobolIDE/issues/439

This repository is a practical fork created to keep OpenCobolIDE usable *today* on a modern Slackware system (tested on Slackware 15.0, Python 3.9).
The goal is simple and finite: have a COBOL IDE that can open a file, compile, run, and show output *without* having to fall back to the terminal every time.
No long-term roadmap, no promise of upstream parity: it exists because I needed it working, and now it does.

The name Opencobolide-4.7.7 is intentionally “one step after” the last upstream release (4.7.6): not because there is a new upstream version,
but because this fork bundles a set of compatibility fixes that make the original codebase run correctly again (even tho it's based of 4.7.4 because thats what I found in SlackBuilds lol).

What changed in this fork
-------------------------

This fork applies a small set of targeted fixes, mostly focused on:

1) Python compatibility
   - Removed reliance on deprecated/removed APIs (e.g. old distro detection via platform.linux_distribution()).
     The objective is not to replace it with another fragile detection mechanism, but to avoid crashing at import time.

2) Qt signal/slot correctness (the “triggered(bool)” problem)
   - Qt actions connected to slots that did not match the expected signature caused warnings like:
     ``QObject::connect: Cannot connect QAction::triggered(bool) to (nullptr)::to_lower()``

     In practice this meant a key assumption (“the editor/action target is always valid at that moment”) was not holding.
     When the action wiring failed, the editor could not reliably operate on the current document state, leading to repeated failures and odd behaviour
     (including situations where UI actions effectively became unusable).
     The fix makes the slots and action creation robust and compatible with the Qt signal signature.

3) Backend / extlibs import reliability
   - OpenCobolIDE bundles a lot of pure-python dependencies in open_cobol_ide/extlibs.
     This is useful, but it also means the import path must be deterministic for both the main process and the backend process.
   - The backend startup script is adjusted so it can always find the bundled libraries without depending on “whatever happens to be first on sys.path”.
   - With total honesty, here I used chatgpt because I had no clue of what I was doing (If i want to run OpenCobolIDE I suppose you understand I am not exacly a Python guy...)

4) Eliminating stdlib shadowing
   - The bundled extlibs contained a module that could shadow Python’s standard library enum module.
     When that happened, Python would lose enum.IntFlag, and even importing re could explode.
     The fix removes that shadowing, restoring correct stdlib behaviour.

The compile action is now guarded: if no file is open, it shows a warning instead of crashing or entering an inconsistent state.
   - Additionally, a logic path could lead to the compile button being disabled “by itself” depending on state transitions.
     This was corrected so the UI reliably allows compiling both executables and modules once the prerequisites are met.

This fork is Slackware-centered
-------------------------------

This work was done and tested on Slackware 15.0 with Python 3.9.
It should be broadly portable, but this fork does not claim universal compatibility.
Slackware’s conservative base and straightforward packaging model make this kind of “keep it working” effort excepitionally practical.

.. image:: doc/Images/slackoff.jpg
    :align: center

If you run it on another distribution and it fails, it will most likely be due to:
- newer Python versions removing additional old APIs used by bundled dependencies,
- different Qt/PyQt packaging and import layouts,
- stricter packaging defaults.

In that case, fixes should still be possible, but they may require additional small patches.

License
-------

OpenCobolIDE is released under the GPL version 3 (and i obviously follow that).

Installation
------------

Slackware
#########

This fork is intended to be built/installed in a Slackware-friendly way (SlackBuild style).
If you are using the SlackBuilds tree, the original packaging approach still applies:
extract source, run the build script, then install the resulting package.

The key difference is that this fork already includes the fixed sources, so you should not need post-install editing.

Other distributions
+++++++++++++++++++

If your system provides Python3, PyQt5, and GnuCOBOL, you can generally install from source.
Because upstream is old and modern build tooling increasingly assumes wheels/PEP517,
a plain setup.py install-style install may be the simplest approach on some systems.

Screenshot
-----------

.. image:: doc/Images/Screenshot.png
    :align: center

Get slack!!!
-----------
.. image:: doc/Images/dobbs.jpg
    :align: center
