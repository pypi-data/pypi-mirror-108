#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PySide6.QtWidgets import QItemDelegate, QDoubleSpinBox, QSpinBox
from PySide6.QtCore import Qt, QAbstractTableModel
import copy
import json

class Float_delegate(QItemDelegate):
	
	def __init__(self, min_value, max_value, dps = 2):
		super(Float_delegate, self).__init__()
		self.min_value = min_value
		self.max_value = max_value
		self.dps = dps
		
	def createEditor(self, parent, option, index):
		spinbox = QDoubleSpinBox(parent)
		if self.max_value is not None:
			spinbox.setMaximum(self.max_value)
		if self.min_value is not None:
			spinbox.setMinimum(self.min_value)
		spinbox.setDecimals(self.dps)
		spinbox.setSingleStep(round(10 ** - (self.dps), self.dps))
		return spinbox

class Int_delegate(QItemDelegate):
	
	def __init__(self, min_value, max_value):
		super(Int_delegate, self).__init__()
		self.min_value = min_value
		self.max_value = max_value
		
	def createEditor(self, parent, option, index):
		spinbox = QSpinBox(parent)
		if self.max_value is not None:
			spinbox.setMaximum(self.max_value)
		if self.min_value is not None:
			spinbox.setMinimum(self.min_value)
		return spinbox

class Table_model(QAbstractTableModel):
	
	def __init__(self, headers, types = {}, editable = [], defaults = {}, delegate_data = {}, header_text = []):
		#headers = list of header names, in order
		#editable = list of headers which are editable
		#types = dict of header : type
		#delegate_data = dict of header : (delegate data) 
		#delegater data is : for int (min, max), float (min, max, dps) 
		#header_text = headers to display
		
		super(Table_model, self).__init__()
		assert(type(types) == dict)
		assert(type(defaults) == dict)
		assert(type(delegate_data) == dict)
		
		
		self.data_store = []
		self.headers = headers.copy()
		
		self.editable = editable.copy()
		
		self.types = {item:str for item in self.headers}
		self.types.update(types)
		
		default_by_type = {str : "", int : 0, float: 0}
		self.defaults = {item:default_by_type[self.types[item]] for item in self.headers}
		self.defaults.update(defaults)
				
		delegate_data_by_type = {str : None, int : (None, None), float: (None, None, 2)}
		self.delegate_data = {item:delegate_data_by_type[self.types[item]] for item in self.headers}
		self.delegate_data.update(delegate_data)
				
		if header_text == []:
			self.header_text = self.headers.copy()
		else:
			self.header_text = header_text.copy()
		
		self.delegates = {}
		
					
	def set_delegates(self, table_widget):
		
		for col_num in range(self.columnCount()):
			col_header = self.headers[col_num]
			col_type = self.types[col_header]
			
			if  col_type == int:
					self.delegates[col_num] = Int_delegate(*self.delegate_data[col_header])
					table_widget.setItemDelegateForColumn(col_num, self.delegates[col_num])
							 
			if col_type == float:
					self.delegates[col_num] = Float_delegate(*self.delegate_data[col_header])
					table_widget.setItemDelegateForColumn(col_num, self.delegates[col_num])
		
		
		
	def rowCount(self, parent = None):
		return len(self.data_store)
		
	def columnCount(self, parent = None):
		return len(self.headers)
		
	def data(self, index, role=Qt.DisplayRole):
		if index.isValid():
			if role == Qt.DisplayRole:
				return str(self.data_store[index.row()][self.headers[index.column()]])
			if role == Qt.EditRole:
				return str(self.data_store[index.row()][self.headers[index.column()]])
		return None

	def setData(self, index, value, role=Qt.EditRole):
		if index.isValid():
			if role == Qt.EditRole:
				if self.types[self.headers[index.column()]] == float:
					self.data_store[index.row()][self.headers[index.column()]] = round(value, self.delegate_data[self.headers[index.column()]][2])
				else:
					self.data_store[index.row()][self.headers[index.column()]] = value
				return True
		return None
	
	def get_json(self):
		return json.dumps(self.data_store)
	
	def get_data(self):
		return copy.deepcopy(self.data_store)
		
	def set_from_json(self, json_data): 
		
		loaded_data = json.loads(json_data)
		self.data_store = []
		for row in loaded_data:
			self.add_row(row)
		self.refresh_all()
	
	def clear(self):
		self.data_store = []
		self.refresh_all()
	
	def flags(self, index):
		if self.headers[index.column()] in self.editable:
			return super(self.__class__,self).flags(index) | Qt.ItemIsEditable 
		else:
			return super(self.__class__,self).flags(index)
	
	def add_row(self, data):
		#data should be a dict
		row = {}
		for header in self.headers:
			if header in data:
				row[header] = data[header]
			else:
				row[header] = self.defaults[header]
		self.data_store.append(row) #probably ought to have some checking here!
		self.refresh_all()

	def del_rows(self, rows):
		rows = list(rows)
		rows.sort(reverse= True)
		for row in rows:
			del self.data_store[row]
		self.refresh_all()
				
	def refresh_all(self):
		self.layoutChanged.emit()
		self.dataChanged.emit(self.index(0,0), self.index(len(self.data_store), len(self.headers)))
	
	def headerData(self, col, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return self.header_text[col]
		return None
	

