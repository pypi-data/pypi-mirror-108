# Copyright (C) 2021 PowerSnail
#
# This file is part of textgrab.
#
# textgrab is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# textgrab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with textgrab.  If not, see <http://www.gnu.org/licenses/>.


"""textgrab.

Usage:
    textgrab 
    textgrab --version
    textgrab (-h | --help)

Options:
    -h --help           Show help
    --version           Print Version
"""

import signal

import docopt
from PySide6 import QtCore, QtWidgets

import textgrab


def ctrl_c_hack(app):
    signal.signal(signal.SIGINT, lambda *_: app.quit())

    _interpreter_hack_timer = QtCore.QTimer(app)
    _interpreter_hack_timer.setInterval(1000)
    _interpreter_hack_timer.timeout.connect(lambda: ...)
    _interpreter_hack_timer.start()


def main():
    args = docopt.docopt(__doc__, version=textgrab.__version__)

    app = QtWidgets.QApplication([textgrab.__name__])
    ctrl_c_hack(app)

    w = textgrab.MainWindow()
    w.show()

    app.exec()
    del w  # Must remove reference to window for cleanup to occur


if __name__ == "__main__":
    main()
