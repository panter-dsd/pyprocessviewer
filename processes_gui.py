# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 00:42:42 2012

@author: panter
"""

import sys
from PySide import QtCore, QtGui
import processes

class ProcessesModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super(ProcessesModel, self).__init__(parent)
        
        self._processes_list = []
        self._processes_list = processes.get_processes_list()
        
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.update_processes_list)
        self._timer.start(500)
        
    def rowCount(self, parent):
        return len(self._processes_list)
        
    def columnCount(self, parent):
        return 3
    
    def data(self, index, role):
        result = None
        
        if role == QtCore.Qt.DisplayRole:
            result = self._processes_list [index.row()].split()[index.column()]
            
        return result
        
    def update_processes_list(self):
        old_processes_lit = self._processes_list
        self._processes_list = processes.get_processes_list()
        
        old_size = len(old_processes_lit)
        new_size = len(self._processes_list)

        if old_size != new_size:
            if old_size < new_size:
                print("insert", old_size, new_size)
                self.beginInsertRows(QtCore.QModelIndex(), old_size, new_size - 1)
                self.endInsertRows()
            else:
                print("remove", old_size, new_size)
                self.beginRemoveRows(QtCore.QModelIndex(), new_size, old_size - 1)
                self.endRemoveRows()
        
        for i in range(min(old_size, new_size)):
            if self._processes_list[i] != old_processes_lit[i]:
                self.dataChanged.emit(self.index(i, 0), 
                                 self.index(i, self.columnCount(None)))
    
        

APP = QtGui.QApplication(sys.argv)

dialog = QtGui.QDialog()
table = QtGui.QTableView(dialog)
model = ProcessesModel(dialog)
table.setModel(model)
layout = QtGui.QHBoxLayout()
layout.addWidget(table)
dialog.setLayout(layout)
dialog.show()

sys.exit(APP.exec_())