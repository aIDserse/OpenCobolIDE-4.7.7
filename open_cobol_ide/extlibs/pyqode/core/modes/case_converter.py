# -*- coding: utf-8 -*-
"""
Contains a case converter mode.
"""
from pyqode.core.api import TextHelper
from pyqode.core.api.mode import Mode
from pyqode.qt import QtCore, QtWidgets


class CaseConverterMode(Mode):
    """Provides context actions for converting case of the selected text."""

    def __init__(self):
        super().__init__()
        self._actions_created = False
        self.action_to_lower = None
        self.action_to_upper = None
        self.menu = None

    @QtCore.Slot(bool)
    def to_upper(self, *args, **kwargs):
        """Converts selected text to upper."""
        if self.editor:
            TextHelper(self.editor).selected_text_to_upper()

    @QtCore.Slot(bool)
    def to_lower(self, *args, **kwargs):
        """Converts selected text to lower."""
        if self.editor:
            TextHelper(self.editor).selected_text_to_lower()

    def _create_actions(self):
        """Create associated actions."""
        if not self.editor:
            return

        self.action_to_lower = QtWidgets.QAction(_('Convert to lower case'), self.editor)
        self.action_to_upper = QtWidgets.QAction(_('Convert to UPPER CASE'), self.editor)

        self.action_to_lower.setShortcut('Ctrl+U')
        self.action_to_upper.setShortcut('Ctrl+Shift+U')

        # Safe connects
        self.action_to_lower.triggered.connect(
            lambda checked=False: self.to_lower(checked)
        )
        self.action_to_upper.triggered.connect(
            lambda checked=False: self.to_upper(checked)
        )

        self.menu = QtWidgets.QMenu(_('Case'), self.editor)
        self.menu.addAction(self.action_to_lower)
        self.menu.addAction(self.action_to_upper)

        self._actions_created = True

    def on_state_changed(self, state):
        if not self.editor:
            return

        if state:
            if not self._actions_created:
                self._create_actions()
            if self.menu:
                self.editor.add_action(self.menu.menuAction())
        else:
            if self.menu:
                self.editor.remove_action(self.menu.menuAction())
