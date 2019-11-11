from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox
from PyQt5 import uic, QtCore, Qt
from main import *

class Window(QMainWindow):
	
	def __init__(self):
	
		#start QMainWindow
		QMainWindow.__init__(self)
		#load file
		uic.loadUi("window.ui",self)
		
		self.initUI()


	def initUI(self):
		self.collect.clicked.connect(lambda: Window())
		#self.consult.clicked.connect(print('consult'))

#start application
app=QApplication(sys.argv)
#Create object class
_window=Window() 
#show window
_window.show()
app.exec_() 
