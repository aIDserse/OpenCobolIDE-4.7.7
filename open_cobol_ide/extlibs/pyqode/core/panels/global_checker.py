"""
This module contains the GlobalCheckerPanel.
"""
from pyqode.core import modes
from pyqode.core.api import Panel, TextHelper
from pyqode.qt import QtCore, QtGui


class GlobalCheckerPanel(Panel):
    """Displays all checker messages found in the document.

    The user can click on a marker to quickly go to the error line.
    """

    def __init__(self):
        super(GlobalCheckerPanel, self).__init__()
        self.scrollable = True

    def _draw_messages(self, painter):
        """
        Draw messages from all subclass of CheckerMode currently installed.
        :type painter: QtGui.QPainter
        """
        checker_modes = []
        for m in self.editor.modes:
            if isinstance(m, modes.CheckerMode):
                checker_modes.append(m)

        mh = self.get_marker_height()
        ms = self.get_marker_size()
        x = self.sizeHint().width() // 4

        for checker_mode in checker_modes:
            for msg in checker_mode.messages:
                block = msg.block
                color = QtGui.QColor(msg.color)
                brush = QtGui.QBrush(color)

                rect = QtCore.QRect()
                rect.setX(int(x))
                rect.setY(int(block.blockNumber() * mh))
                rect.setSize(ms)

                painter.fillRect(rect, brush)

    def _draw_visible_area(self, painter):
        """
        Draw the visible area (does not take folded blocks into account).
        :type painter: QtGui.QPainter
        """
        if self.editor.visible_blocks:
            start = self.editor.visible_blocks[0][-1]
            end = self.editor.visible_blocks[-1][-1]

            mh = self.get_marker_height()

            rect = QtCore.QRect()
            rect.setX(0)
            rect.setY(int(start.blockNumber() * mh))
            rect.setWidth(int(self.sizeHint().width()))
            rect.setBottom(int(end.blockNumber() * mh))

            if self.editor.background.lightness() < 128:
                c = self.editor.background.darker(150)
            else:
                c = self.editor.background.darker(110)
            c.setAlpha(128)

            painter.fillRect(rect, c)

    def paintEvent(self, event):
        """
        Paints the messages and the visible area on the panel.
        :param event: paint event infos
        """
        if not self.isVisible():
            return

        painter = QtGui.QPainter(self)
        try:
            # fill background
            self._background_brush = QtGui.QBrush(self.editor.background)
            painter.fillRect(event.rect(), self._background_brush)

            self._draw_messages(painter)
            self._draw_visible_area(painter)
        finally:
            painter.end()

    def sizeHint(self):
        """
        The panel has a fixed width of 12 pixels.
        """
        return QtCore.QSize(12, 16)

    def get_marker_height(self):
        """
        Gets the height (in pixels) of a message marker.
        Always returns an int >= 1 (Qt needs ints here).
        """
        line_count = TextHelper(self.editor).line_count()
        if line_count <= 0:
            line_count = 1

        mh = self.editor.viewport().height() / line_count  # float
        if mh < 1:
            return 1
        return int(mh)

    def get_marker_size(self):
        """
        Gets the size of a message marker.
        :return: QSize (ints only)
        """
        h = self.get_marker_height()
        w = self.sizeHint().width() // 2
        if w < 1:
            w = 1
        if h < 1:
            h = 1
        return QtCore.QSize(int(w), int(h))

    def mousePressEvent(self, event):
        """
        Moves the editor text cursor to the clicked line.
        """
        mh = self.get_marker_height()
        if mh <= 0:
            mh = 1

        height = event.pos().y()
        line = height // mh  # int // int -> int
        TextHelper(self.editor).goto_line(int(line))
