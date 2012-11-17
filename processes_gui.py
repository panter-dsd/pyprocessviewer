# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 00:42:42 2012

@author: panter
"""

import sys
from PySide import QtCore, QtGui
import processes

class ProcessesModel(QtCore.QAbstractTableModel):
    """ProcessesModel"""
    def __init__(self, parent=None):
        """__init__"""
        QtCore.QAbstractTableModel.__init__(self, parent)
        
        self._processes_list = []
        self._processes_list = processes.get_processes_list()
        
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.update_processes_list)
        self._timer.start(500)
    
    def rowCount(self, _parent = QtCore.QModelIndex()):
        """rowCount"""
        return len(self._processes_list)
    
    def columnCount(self, _parent = QtCore.QModelIndex()):
        """columnCount"""
        return 3
    
    def data(self, index, role):
        """data"""
        result = None
        
        if role == QtCore.Qt.DisplayRole:
            result = self._processes_list [index.row()].split()[index.column()]
            
        return result
        
    def update_processes_list(self):
        """update_processes_list"""
        old_processes_lit = self._processes_list
        self._processes_list = processes.get_processes_list()
        
        old_size = len(old_processes_lit)
        new_size = len(self._processes_list)

        if old_size != new_size:
            if old_size < new_size:
                QtCore.QAbstractTableModel.beginInsertRows(self,
                                                           QtCore.QModelIndex(), 
                                                           old_size, 
                                                           new_size - 1)
                QtCore.QAbstractTableModel.endInsertRows(self)
            else:
                QtCore.QAbstractTableModel.beginRemoveRows(self,
                                                           QtCore.QModelIndex(), 
                                                           new_size, 
                                                           old_size - 1)
                QtCore.QAbstractTableModel.endRemoveRows(self)
        
        for i in range(min(old_size, new_size)):
            if self._processes_list[i] != old_processes_lit[i]:
                self.dataChanged.emit(QtCore.QAbstractTableModel.index(self, i, 0), 
                                      QtCore.QAbstractTableModel.index(self, i, self.columnCount(None)))
    
        
if __name__ == "__main__":
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