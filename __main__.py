# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 12:33:33 2012

@author: panter
"""

import sys
from PySide import QtGui
import processes_gui


def main():
    """main"""
    app = QtGui.QApplication(sys.argv)

    dialog = QtGui.QDialog()
    table = QtGui.QTableView(dialog)
    model = processes_gui.ProcessesModel(dialog)
    table.setModel(model)
    layout = QtGui.QHBoxLayout()
    layout.addWidget(table)
    dialog.setLayout(layout)
    dialog.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()