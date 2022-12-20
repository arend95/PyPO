from PyQt5.QtWidgets import QWidget, QLabel,QSpacerItem, QSizePolicy, QLineEdit, QHBoxLayout, QPushButton
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
import sys
from numpy import array

from src.GUI.ParameterForms.InputDescription import *

Validator_floats = QRegExpValidator(QRegExp("[-+]?[0-9]*[\.,]?[0-9]*"))
Validator_ints = QRegExpValidator(QRegExp("[-+]?[0-9]*"))


class SimpleInput(QWidget):
    def __init__ (self, inp:InputDescription):
        super().__init__()
        self.inputDescription = inp

        self.layout = QHBoxLayout()
        self.setupUI()
        # self.makeTestBtn()
        self.setLayout(self.layout)

    def setupUI(self):
        inp = self.inputDescription
        
        self.inputs = [QLineEdit() for k in range(inp.numFields)]
        # validator = 
        for edit in self.inputs:
            edit.setValidator(None)
        editLayout = QHBoxLayout()
        
        for i in range(inp.numFields):
            edit = self.inputs[i]
            edit.setPlaceholderText(str(inp.hints[i]))
            editLayout.addWidget(edit)
        self.editsWid = QWidget()
        self.editsWid.setLayout(editLayout)

        self.label = self.makeLabelFromString(self.inputDescription.label)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.editsWid)
    
    def read(self):
        l =[self.enumToType(self.inputDescription.inType)(i.text()) for i in self.inputs] 
        if len(l)>1:        
            if self.inputDescription.oArray:
                l = array(l)
        else:
            l = l[0]
        l = {self.inputDescription.outputName:l}
        return l

    @staticmethod
    def enumToType(intype):
        if intype == inType.integers: return int
        if intype == inType.floats: return float
        if intype == inType.string: return str

    @staticmethod
    def makeLabelFromString(s):
        if type(s) == str:
            return QLabel(s.replace("_"," ").capitalize())
        else: return QLabel(s)
