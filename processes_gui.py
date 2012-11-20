# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 00:42:42 2012

@author: panter
"""

from PySide import QtCore
import processes


class ProcessesModel(QtCore.QAbstractTableModel):
    """ProcessesModel"""
    def __init__(self, parent=None):
        """__init__"""
        super(ProcessesModel, self).__init__(parent)

        self._processes_list = []
        self._processes_list = processes.get_processes_list()

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.update_processes_list)
        self._timer.start(500)

    def rowCount(self, _parent = QtCore.QModelIndex()):
        """rowCount"""
        return len(self._processes_list)

    def columnCount(self, _parent=QtCore.QModelIndex()):
        """columnCount"""
        return 3

    def headerData(self,
                   section,
                   orientation,
                   role = QtCore.Qt.DisplayRole):
        """headerData"""
        header_map = dict()
        header_map[0] = "Status"
        header_map[1] = "Status string"
        header_map[2] = "Cmd"

        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            result = header_map[section]
        else:
            result = super(ProcessesModel, self).headerData(section,
                                                            orientation,
                                                            role)
        return result

    def data(self, index, role):
        """data"""
        result = None

        if role == QtCore.Qt.DisplayRole:
            result = self._processes_list[index.row()].split()[index.column()]

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
                                                           QtCore.QModelIndex(
                                                           ),
                                                           old_size,
                                                           new_size - 1)
                QtCore.QAbstractTableModel.endInsertRows(self)
            else:
                QtCore.QAbstractTableModel.beginRemoveRows(self,
                                                           QtCore.QModelIndex(
                                                           ),
                                                           new_size,
                                                           old_size - 1)
                QtCore.QAbstractTableModel.endRemoveRows(self)

        for i in range(min(old_size, new_size)):
            if self._processes_list[i] != old_processes_lit[i]:
                self.dataChanged.emit(
                    QtCore.QAbstractTableModel.index(self, i, 0),
                    QtCore.QAbstractTableModel.index(self,
                                                     i,
                                                     self.columnCount(None)))
