from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MySlider(QSlider):

	########################################
	#
	########################################
	def mousePressEvent (self, event):
		opt = QStyleOptionSlider()
		self.initStyleOption(opt)
		sr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)
		if event.button() == Qt.LeftButton and not sr.contains(event.pos()):
			newVal = self.minimum() + ((self.maximum()-self.minimum()) * event.x()) / self.width()
			if self.invertedAppearance():
				self.setValue(self.maximum() - newVal)
			else:
				self.setValue(newVal)
			event.accept()
		super().mousePressEvent(event)
