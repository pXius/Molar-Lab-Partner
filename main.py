from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from lib.molarmass import Formula

class Ui(QtWidgets.QMainWindow):
	def __init__(self):
		super(Ui, self).__init__() # Call the inherited classess __init__ method
		uic.loadUi('Main.ui', self) # Load the .ui file
		self.show() # Show the GUI

		# Linking Inputs to Functions
		# Button Clicks
		self.b1.clicked.connect(lambda: self.b1clicked(Formula(str(self.formulaInput.toPlainText()))))
		self.b2.clicked.connect(lambda: self.b2clicked(Formula(str(self.formulaInput.toPlainText())),self.subGram.toPlainText()))
		self.b3.clicked.connect(lambda: self.b3clicked())
		self.b4.clicked.connect(lambda: self.b4clicked())
		self.b5.clicked.connect(lambda: self.b5clicked())
		self.b6.clicked.connect(lambda: self.b6clicked())
		self.b7.clicked.connect(lambda: self.b7clicked())
		
		#Radio Button Toggles
		self.radsol.toggled.connect(lambda: self.radsolon())
		self.radmol.toggled.connect(lambda: self.radmolon())
		self.radvol.toggled.connect(lambda: self.radvolon())
		self.radmol2.toggled.connect(lambda: self.radmol2on())
		self.radvol2.toggled.connect(lambda: self.radvol2on())
		self.radvol1.toggled.connect(lambda: self.radvol1on())
		
		#Action Menu
		self.actionExit.triggered.connect(lambda: quit())
		self.actionDisclaimer.triggered.connect(lambda: self.disclaimerpop.exec_())
		self.actionAbout.triggered.connect(lambda: self.aboutpop.exec_())

		#Check Boxes
		self.weightCheck.stateChanged.connect(self.weightCheckChange)
		self.nonMolar.stateChanged.connect(self.nonMolarChange)

		# Some UI default settings
		self.reqweight.setHidden(True)
		self.molarity.setReadOnly(True)
		self.disclaimerpop()
		self.about()
		self.font = QtGui.QFont()
		self.font.setFamily("Lato")
		self.font.setPointSize(12)
		self.molarity.setStyleSheet("background-color: rgb(197, 215, 255);")
		self.molarity.setFont(self.font)
		self.molarity2.setStyleSheet("background-color: rgb(197, 215, 255);")
		self.molarity2.setFont(self.font)		
		self.formulaInput.setFocus()
		self.molarityCombo1.view().setRowHidden(3, True)
		self.molarityCombo2.view().setRowHidden(3, True)
		self.volumeCombo1.view().setRowHidden(3, True)
		self.volumeCombo2.view().setRowHidden(3, True)

		# Base calculation values
		self.resetBackend()

		# Tab4 Radio Button Grouping
		self.tab4rad = QtWidgets.QButtonGroup(self)
		self.tab4rad.addButton(self.radvol1)
		self.tab4rad.addButton(self.radvol2)
		self.tab4rad.addButton(self.radmol2)


	#***************************************************************************************************************************
	# Message Boxes*************************************************************************************************************

	# Value Errors
	def recverror(self):
		self.verror = QMessageBox()
		self.verror.setIcon(QMessageBox.Warning)
		self.verror.setWindowTitle("Input Error!")
		self.verror.setText("Missing or non-numerical value!"+25*" ")
		self.verror.setInformativeText("Click 'Show Details' for more information.")
		self.verror.setDetailedText("Input values needs to be numerical.\nMake sure you are using a . period as a decimal seperator.\nExamples: 10.5  0.05  1.025")
		self.verror.buttonClicked.connect(lambda: self.recverror())

	# Formula Errors
	def recferror(self, e):
		self.ferror = QMessageBox()
		self.formulaInput.setPlainText("")
		self.ferror.setIcon(QMessageBox.Warning)
		self.ferror.setWindowTitle('Formula Error!')
		self.ferror.setText(str('{}!'.format(e.message.capitalize()))+45*" ")
		self.ferror.setInformativeText("Click 'Show Details' for more information.")
		self.ferror.setDetailedText("That is not a vaild formula!\nFormulas are CaSe-sEnSaTivE.\n\nExamples of valid formulas are:\nH2O, [2H]2O, CaCl2, Au, CH3COOH, EtOH, CuSO4.5H2O, (COOH)2, AgCuRu4(H)2[CO]12{PPh3}2, CGCGAATTCGCG, and MDRGEQGLLK\n\nCopy/Pasting from web pages where special characters or text formatting is used, can cause errors.\nTry entering the formula manually.")
		self.ferror.buttonClicked.connect(lambda: self.recferror(e))

	# ZeroDiv Errors
	def reczerror(self):
		 self.zerror = QMessageBox()
		 self.zerror.setIcon(QMessageBox.Warning)
		 self.zerror.setWindowTitle('Zero Division Error!')
		 self.zerror.setText(str("Missing or 0 value input!"+35*" "))
		 self.zerror.setInformativeText("Click 'Show Details' for more information.")
		 self.zerror.setDetailedText("The calculator equation is attempting to divide by zero based on one of your set or missing input values.\n\nWe can't do that because... math.")
		 self.zerror.buttonClicked.connect(lambda: self.reczerror())

	# Disclaimer Popup
	def disclaimerpop(self):
		 self.disclaimerpop = QMessageBox()
		 self.disclaimerpop.setIcon(QMessageBox.Information)
		 self.disclaimerpop.setWindowTitle('Disclaimer!')
		 self.disclaimerpop.setText("\nBecause this application is provided free of charge, there is\nno warranty for this application or it's performance,\nto the extent permitted by applicable law.\n\nThis application is provided 'as is' without warranty of any kind, either expressed or implied, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose.\n\nThe entire risk as to the quality and performance is with you.\n")

	# V2 Lower than V1
	def v2lowerError(self):
		 self.v2v1error = QMessageBox()
		 self.v2v1error.setIcon(QMessageBox.Warning)
		 self.v2v1error.setWindowTitle('Desired Volume too low!')
		 self.v2v1error.setText(str("The Desired Solution Volume (V2) needs to be\nequal or higher than the Stock Solution Volume (V1)!"+30*" "))
		 self.molarity2.setPlainText("")
		 self.volume2.setPlainText("")
		 self.addSol.setText("")
		 self.addDil.setText("")

	def emptyFormula(self):
		self.emptyForError = QMessageBox()
		self.formulaInput.setPlainText("")
		self.emptyForError.setIcon(QMessageBox.Warning)
		self.emptyForError.setWindowTitle('Formula Error!')
		self.emptyForError.setText("In order to calculare a higher desired molarity,\n(M2 > M1) you need to provide an elemantal formula!")
		self.emptyForError.setDetailedText("That is not a vaild formula!\nFormulas are CaSe-sEnSaTivE.\n\nExamples of valid formulas are:\nH2O, [2H]2O, CaCl2, Au, CH3COOH, EtOH, CuSO4.5H2O, (COOH)2, AgCuRu4(H)2[CO]12{PPh3}2, CGCGAATTCGCG, and MDRGEQGLLK\n\nCopy/Pasting from web pages where special characters or text formatting is used, can cause errors.\nTry entering the formula manually.")
		self.clearAdds()
		self.volume2.setPlainText("")
		self.emptyForError.buttonClicked.connect(lambda: self.emptyFormula())

	def zeroVolume1(self):
		self.zeroVolError = QMessageBox()
		self.clear_tab_4()
		self.clearAdds()
		self.zeroVolError.setIcon(QMessageBox.Warning)
		self.zeroVolError.setWindowTitle('No Stock Volume!')
		self.zeroVolError.setText("You need a Stock Volume (V1) higher than 0!")


	def about(self):
		self.aboutpop = QMessageBox()
		self.aboutpop.setIcon(QMessageBox.Information)
		self.aboutpop.setWindowTitle('About:')
		self.aboutpop.setText(10*" "+"Molar Lab Partner"+20*" "+"\n\n"+15*" "+"Version 1.0"+"\n\n"+22*" "+"by"+"\n\n"+6*" "+"Hermanus Engelbrecht"+"\n"+2*" " + "fan.engelbrecht@gmail.com" +"\n\n")

	def generalMode(self):
		self.generalModepop = QMessageBox()
		self.generalModepop.setIcon(QMessageBox.Information)
		self.generalModepop.setWindowTitle('General Dilution Mode')
		self.generalModepop.setText('When using General Dilution Mode:'+30*" "+'\n\nMake sure to use the same unit of measurement\nfor both M1, M2 and V1, V2.\n\nClick Details for an example.')
		self.generalModepop.setDetailedText("Using the same unit of measurement for M1, M2 and V1, V2:\nM1 = 100g\nM2 = 1500g\nV1 = 0.4 Liters\nV2 = 1.3 Liters\nNote how both parameters share the same units of measurement.")
		self.generalModepop.exec_()

	#***************************************************************************************************************************
	# Number & Decimal handling*************************************************************************************************

	# Reset backend Values to 0
	def resetBackend(self):
		self.M = 0
		self.n = 0
		self.V = 0
		self.M1 = 0
		self.M2 = 0
		self.V1 = 0
		self.V2 = 0
		self.n1 = 0
		self.n2 = 0
		self.n3 = 0
		self.addSolValue = ""
		self.addDilValie = ""

	def checkVol1(self):
		if self.volume1.toPlainText() == 0.0 or self.volume1.toPlainText() == "":
			self.zeroVolume1()
			self.zeroVolError.exec_()
			self.clearAdds()
			self.clear_tab_4()

	# Normalize values for calculations
	def decimal_norm(self):
		# Molarity Check
		if self.molarity.toPlainText() == "":
			self.molarity.setPlainText('0')	
		if self.molarityCombo.currentText() == 'Molar (M)':
			self.M = float(self.molarity.toPlainText())
		elif self.molarityCombo.currentText() == 'Millimolar (mM)':
			self.M = float(self.molarity.toPlainText())/1000
		elif self.molarityCombo.currentText() == 'Micromolar (uM)':
			self.M = float(self.molarity.toPlainText())/1000000
		#Moles of Solute Check
		if self.molValueOutput2.toPlainText() == "":
			self.molValueOutput2.setPlainText('0')	
		if self.molarityCombo_2.currentText() == 'Molar (M)':
			self.n = float(self.molValueOutput2.toPlainText())
		elif self.molarityCombo_2.currentText() == 'Millimolar (mM)':
			self.n = float(self.molValueOutput2.toPlainText())/1000
		elif self.molarityCombo_2.currentText() == 'Micromolar (uM)':
			self.n = float(self.molValueOutput2.toPlainText())/1000000
		#Value Check
		if self.volume.toPlainText() == "":
			self.volume.setPlainText('0')
		if self.volumeCombo.currentText() == 'Liter (L)':
			self.V = float(self.volume.toPlainText())
		elif self.volumeCombo.currentText() == 'Milliliter (ml)':
			self.V = float(self.volume.toPlainText())/1000
		elif self.volumeCombo.currentText() == 'Microliter (ul)':
			self.V = float(self.volume.toPlainText())/1000000

	# Restore normalized values to requested format
	def decimal_unnorm(self):
		# Molarity Check
		if self.molarityCombo.currentText() == 'Molar (M)':
			self.M = self.M * 1
		elif self.molarityCombo.currentText() == 'Millimolar (mM)':
			self.M = self.M * 1000
		elif self.molarityCombo.currentText() == 'Micromolar (uM)':
			self.M = self.M * 1000000
		# Moles of Soulte Check
		if self.molarityCombo_2.currentText() == 'Molar (M)':
			self.n = self.n * 1
		elif self.molarityCombo_2.currentText() == 'Millimolar (mM)':
			self.n = self.n * 1000
		elif self.molarityCombo_2.currentText() == 'Micromolar (uM)':
			self.n = self.n * 1000000
		# Volume Check
		if self.volumeCombo.currentText() == 'Liter (L)':
			self.V = self.V * 1
		elif self.volumeCombo.currentText() == 'Milliliter (ml)':
			self.V = self.V * 1000
		elif self.volumeCombo.currentText() == 'Microliter (ul)':
			self.V = self.V * 1000000

	# Send values to output boxes Tab 3
	def print_values(self):
		self.molarity.setPlainText(str(round(self.M, 6)))
		self.molValueOutput2.setPlainText(str(round(self.n, 6)))
		self.volume.setPlainText(str(round(self.V, 6)))

	def decimal_norm2(self):
		# Molarity1 Check
		if self.molarity1.toPlainText() == "":
			self.molarity1.setPlainText('0')	
		if self.molarityCombo1.currentText() == 'Molar (M)':
			self.M1 = float(self.molarity1.toPlainText())
		elif self.molarityCombo1.currentText() == 'Millimolar (mM)':
			self.M1 = float(self.molarity1.toPlainText())/1000
		elif self.molarityCombo1.currentText() == 'Micromolar (uM)':
			self.M1 = float(self.molarity1.toPlainText())/1000000
		elif self.molarityCombo1.currentText() == 'Custom':
			self.M1 = float(self.molarity1.toPlainText())

		# Molarity2 Check
		if self.molarity2.toPlainText() == "":
			self.molarity2.setPlainText('0')	
		if self.molarityCombo2.currentText() == 'Molar (M)':
			self.M2 = float(self.molarity2.toPlainText())
		elif self.molarityCombo2.currentText() == 'Millimolar (mM)':
			self.M2 = float(self.molarity2.toPlainText())/1000
		elif self.molarityCombo2.currentText() == 'Micromolar (uM)':
			self.M2 = float(self.molarity2.toPlainText())/1000000
		elif self.molarityCombo2.currentText() == 'Custom':
			self.M2 = float(self.molarity2.toPlainText())

		#Value1 Check
		if self.volume1.toPlainText() == "":
			self.volume1.setPlainText('0')
		if self.volumeCombo1.currentText() == 'Liter (L)':
			self.V1 = float(self.volume1.toPlainText())
		elif self.volumeCombo1.currentText() == 'Milliliter (ml)':
			self.V1 = float(self.volume1.toPlainText())/1000
		elif self.volumeCombo1.currentText() == 'Microliter (ul)':
			self.V1 = float(self.volume1.toPlainText())/1000000
		elif self.volumeCombo1.currentText() == 'Custom':
			self.V1 = float(self.volume1.toPlainText())

		#Value2 Check
		if self.volume2.toPlainText() == "":
			self.volume2.setPlainText('0')
		if self.volumeCombo2.currentText() == 'Liter (L)':
			self.V2 = float(self.volume2.toPlainText())
		elif self.volumeCombo2.currentText() == 'Milliliter (ml)':
			self.V2 = float(self.volume2.toPlainText())/1000
		elif self.volumeCombo2.currentText() == 'Microliter (ul)':
			self.V2 = float(self.volume2.toPlainText())/1000000
		elif self.volumeCombo2.currentText() == 'Custom':
			self.V2 = float(self.volume2.toPlainText())

	def decimal_unnorm2(self):
		# Molarity1 Check
		if self.molarityCombo1.currentText() == 'Molar (M)':
			self.M1 = self.M1 * 1
		elif self.molarityCombo1.currentText() == 'Millimolar (mM)':
			self.M1 = self.M1 * 1000
		elif self.molarityCombo1.currentText() == 'Micromolar (uM)':
			self.M1 = self.M1 * 1000000

		# Molarity2 Check
		if self.molarityCombo2.currentText() == 'Molar (M)':
			self.M2 = self.M2 * 1
		elif self.molarityCombo2.currentText() == 'Millimolar (mM)':
			self.M2 = self.M2 * 1000
		elif self.molarityCombo2.currentText() == 'Micromolar (uM)':
			self.M2 = self.M2 * 1000000

		# Volume1 Check
		if self.volumeCombo1.currentText() == 'Liter (L)':
			self.V1 = self.V1 * 1
		elif self.volumeCombo1.currentText() == 'Milliliter (ml)':
			self.V1 = self.V1 * 1000
		elif self.volumeCombo1.currentText() == 'Microliter (ul)':
			self.V1 = self.V1 * 1000000

		# Volume2 Check
		if self.volumeCombo2.currentText() == 'Liter (L)':
			self.V2 = self.V2 * 1
		elif self.volumeCombo2.currentText() == 'Milliliter (ml)':
			self.V2 = self.V2 * 1000
		elif self.volumeCombo2.currentText() == 'Microliter (ul)':
			self.V2 = self.V2 * 1000000

	# Send tab4 values to output boxes
	def print_values2(self):
		self.molarity1.setPlainText(str(round(self.M1, 6)))
		self.volume1.setPlainText(str(round(self.V1, 6)))
		self.molarity2.setPlainText(str(round(self.M2, 6)))
		self.volume2.setPlainText(str(round(self.V2, 6)))

	# Print to addDil
	def printAddDil(self):
		if self.addDilCombo.currentText() == 'Liter (L)':
			self.addDil.setStyleSheet("background-color: rgb(197, 215, 255);")
			self.addDil.setFont(self.font)
			self.addDil.setText(str(round((self.V2 - self.V1), 6)))
		elif self.addDilCombo.currentText() == 'Milliliter (ml)':
			self.addDil.setStyleSheet("background-color: rgb(197, 215, 255);")
			self.addDil.setFont(self.font)
			self.addDil.setText(str(round((self.V2 - self.V1)*1000, 6)))			
		elif self.addDilCombo.currentText() == 'Microliter (ul)':
			self.addDil.setStyleSheet("background-color: rgb(197, 215, 255);")
			self.addDil.setFont(self.font)
			self.addDil.setText(str(round((self.V2 - self.V1)*1000000, 6)))	

	def printAddSol(self):
		if self.addSolCombo.currentText() == 'Grams (g)':
			self.addSol.setStyleSheet("background-color: rgb(197, 215, 255);")
			self.addSol.setFont(self.font)
			self.addSolValue = self.n3 * Formula(str(self.formulaInput.toPlainText())).mass
			self.addSol.setText(str(round(self.addSolValue, 6)))
		else:
			self.addSol.setStyleSheet("background-color: rgb(197, 215, 255);")
			self.addSol.setFont(self.font)
			self.addSolValue = self.n3 * Formula(str(self.formulaInput.toPlainText())).mass
			self.addSol.setText(str(round((self.addSolValue)*1000, 6)))

	#********************************************************************************************************************
	# Tab Clearing*******************************************************************************************************
	
	def clear_tab_1(self):
		self.massOutput.setText("")

	def clear_tab_2(self):
		self.subGram.setPlainText("")
		self.molValueOutput.setText("")

	def clear_tab_3(self):
		self.subGram2.setPlainText("")
		self.molarity.setPlainText("")
		self.volume.setPlainText("")
		self.molValueOutput2.setPlainText("")

	def clear_tab_4(self):
		self.molarity1.setPlainText("")
		self.molarity2.setPlainText("")
		self.volume1.setPlainText("")
		self.volume2.setPlainText("")
		self.clearAdds()

	def clearAdds(self):
		self.addSol.setText("")
		self.addSol.setStyleSheet("background-color: rgb(255, 255, 255);")
		self.addSol.setFont(self.font)
		self.addDil.setText("")
		self.addDil.setStyleSheet("background-color: rgb(255, 255, 255);")
		self.addDil.setFont(self.font)

	#********************************************************************************************************************
	# Button Clicks******************************************************************************************************
	
	# Calculate Molar Mass of Formula Tab 1
	def b1clicked(self, formula):
		self.clear_tab_2()
		self.clear_tab_3()
		try:
			self.massOutput.setText('Empirical Formula:\t' + str(formula.empirical))
			self.massOutput.append('Molecular Mass:\t' + str(round(formula.mass, 7)))
			self.massOutput.append(str(formula.composition()))
		except Exception as e:
			self.recferror(e)
			self.ferror.exec_()
			self.massOutput.setText("")

	# Calculate Mass of Solute for Tab 2 when button is pressed.
	def b2clicked(self, formula, subGram):
		self.clear_tab_1()
		self.clear_tab_3()
		try:
			if self.soluteWeight.currentText() == "Grams (g)":
				self.molValueOutput.setText('Mass of Solute:    ' + str(round((float(subGram)/formula.mass), 7)))
			else:
				self.molValueOutput.setText('Mass of Solute:    ' + str(round(((float(subGram)/1000)/formula.mass), 7)))
		except ValueError:
			self.recverror()
			self.verror.exec_()
			self.molValueOutput.setText("")
			self.subGram.setPlainText("")
		except Exception as e:
			self.recferror(e)
			self.ferror.exec_()

	# Calculated Tab3 variabled based on radio button selection.
	def b3clicked(self):
		self.clear_tab_1()
		self.clear_tab_2()
		self.clear_tab_4()
		if self.radmol.isChecked():
			self.molaritybox()
		elif self.radsol.isChecked():
			self.solutebox()
		elif self.radvol.isChecked():
			self.volbox()

	# Import Tab3 values to Tab4
	def b4clicked(self):
		self.clear_tab_1()
		self.clear_tab_2()
		self.clearAdds()
		self.decimal_norm()
		self.M1 = self.M
		self.V1 = self.V
		self.decimal_unnorm2()
		self.molarity1.setPlainText(str(round((self.M1), 6)))
		self.volume1.setPlainText(str(round((self.V1), 6)))

	# Calculate Tab4 Variables based on radio button selection
	def b5clicked(self):
		self.clear_tab_1()
		self.clear_tab_2()
		self.clearAdds()
		if self.nonMolar.isChecked():
			self.nonMolarCalc()
		elif self.radmol2.isChecked():
			self.molbox2()
		elif self.radvol2.isChecked():
			self.volbox2()
		elif self.radvol1.isChecked():
			self.volbox1()

	# Clear tab 3
	def b6clicked(self):
		self.clear_tab_3()

	# Clear tab 4
	def b7clicked(self):
		self.clear_tab_4()

	#***********************************************************************************************************************
	# Radio Button and Checkbox Toggles**************************************************************************************************

	def radsolon(self):
		if self.radsol.isChecked():
			self.molValueOutput2.setPlainText("")
			self.molValueOutput2.setReadOnly(True)
			self.subGram2.setPlainText("")
			self.subGram2.setReadOnly(True)
			self.weightCheck.setEnabled(False)
			self.weightCheck.setChecked(False)
			self.reqweight.show()
			self.reqweight.setHidden(False)
			self.subGram2.setStyleSheet("background-color: rgb(197, 215, 255);")
			self.molValueOutput2.setStyleSheet("background-color: rgb(197, 215, 255);")
			self.subGram2.setFont(self.font)
			self.molValueOutput2.setFont(self.font)
			self.molarityCombo_2.setCurrentIndex(0)
			self.molarityCombo_2.setEnabled(False)
		else:
			self.weightCheck.setEnabled(True)
			self.reqweight.hide()
			self.reqweight.setHidden(True)
			self.subGram2.setReadOnly(False)
			self.molValueOutput2.setReadOnly(False)
			self.subGram2.setStyleSheet("background-color: rgb(255, 255, 255);")
			self.molValueOutput2.setStyleSheet("background-color: rgb(255, 255, 255);")			
			self.subGram2.setFont(self.font)
			self.molValueOutput2.setFont(self.font)
			self.molarityCombo_2.setEnabled(True)

	def radmolon(self):
		if self.radmol.isChecked():
			self.molarity.setPlainText("")
			self.molarity.setReadOnly(True)
			self.molarity.setStyleSheet("background-color: rgb(197, 215, 255);")
			self.molarity.setFont(self.font)
		else:
			self.molarity.setReadOnly(False)
			self.molarity.setStyleSheet("background-color: rgb(255, 255, 255);")
			self.molarity.setFont(self.font)

	def radvolon(self):
		if self.radvol.isChecked():
			self.volume.setPlainText("")
			self.volume.setReadOnly(True)
			self.volume.setStyleSheet("background-color: rgb(197, 215, 255);")
			self.volume.setFont(self.font)
		else:
			self.volume.setReadOnly(False)
			self.volume.setStyleSheet("background-color: rgb(255, 255, 255);")
			self.volume.setFont(self.font)

	# SolWeight Checkbox State Change
	def weightCheckChange(self, state):
		if self.weightCheck.isChecked():
			self.molValueOutput2.setStyleSheet("background-color: rgb(197, 215, 255);")
		else:
			self.molValueOutput2.setStyleSheet("background-color: rgb(255, 255, 255);")

	# Non Molar State
	def nonMolarChange(self):
		if self.nonMolar.isChecked():
			self.molarityCombo1.view().setRowHidden(3, False)
			self.molarityCombo2.view().setRowHidden(3, False)
			self.volumeCombo1.view().setRowHidden(3, False)
			self.volumeCombo2.view().setRowHidden(3, False)
			self.molarityCombo1.setCurrentIndex(3)
			self.molarityCombo2.setCurrentIndex(3)
			self.volumeCombo1.setCurrentIndex(3)
			self.volumeCombo2.setCurrentIndex(3)
			self.molarityCombo1.setEnabled(False)
			self.molarityCombo2.setEnabled(False)
			self.volumeCombo1.setEnabled(False)
			self.volumeCombo2.setEnabled(False)
			self.addSolCombo.setEnabled(False)
			self.addDilCombo.setEnabled(False)
			self.label_28.setEnabled(False)
			self.label_29.setEnabled(False)
			self.label_24.setText("M1")
			self.radvol1.setText("V1")
			self.radmol2.setText("M2")
			self.radvol2.setText("V2")
			self.generalMode()
		else:
			self.molarityCombo1.view().setRowHidden(3, True)
			self.molarityCombo2.view().setRowHidden(3, True)
			self.volumeCombo1.view().setRowHidden(3, True)
			self.volumeCombo2.view().setRowHidden(3, True)
			self.molarityCombo1.setCurrentIndex(0)
			self.molarityCombo2.setCurrentIndex(0)
			self.volumeCombo1.setCurrentIndex(0)
			self.volumeCombo2.setCurrentIndex(0)
			self.molarityCombo1.setEnabled(True)
			self.molarityCombo2.setEnabled(True)
			self.volumeCombo1.setEnabled(True)
			self.volumeCombo2.setEnabled(True)
			self.addSolCombo.setEnabled(True)
			self.addDilCombo.setEnabled(True)
			self.label_28.setEnabled(True)
			self.label_29.setEnabled(True)
			self.label_24.setText("Molarity (M1)")
			self.radvol1.setText("Volume (V1)")
			self.radmol2.setText("Molarity (M2)")
			self.radvol2.setText("Volume (V2)")


	# Dilution Tab Radio Buttons
	def radmol2on(self):
		if self.radmol2.isChecked():
			self.molarity2.setPlainText("")
			self.molarity2.setReadOnly(True)
			self.molarity2.setStyleSheet("background-color: rgb(197, 215, 255);")
			self.molarity2.setFont(self.font)
			self.clearAdds()
		else:
			self.molarity2.setReadOnly(False)
			self.molarity2.setStyleSheet("background-color: rgb(255, 255, 255);")
			self.molarity2.setFont(self.font)

	def radvol1on(self):
		if self.radvol1.isChecked():
			self.volume1.setPlainText("")
			self.volume1.setReadOnly(True)
			self.volume1.setStyleSheet("background-color: rgb(197, 215, 255);")
			self.volume1.setFont(self.font)
			self.clearAdds()
		else:
			self.volume1.setReadOnly(False)
			self.volume1.setStyleSheet("background-color: rgb(255, 255, 255);")
			self.volume1.setFont(self.font)

	def radvol2on(self):
		if self.radvol2.isChecked():
			self.volume2.setPlainText("")
			self.volume2.setReadOnly(True)
			self.volume2.setStyleSheet("background-color: rgb(197, 215, 255);")
			self.volume2.setFont(self.font)
			self.clearAdds()
		else:
			self.volume2.setReadOnly(False)
			self.volume2.setStyleSheet("background-color: rgb(255, 255, 255);")
			self.volume2.setFont(self.font)




	#***********************************************************************************************************************
	# Molarity Tab Calculations Tab 3*********************************************************************************************

	# Calculate Solute Mass off of available Weight IF box is ticked.
	def mos(self):
		if self.soluteWeight2.currentText() == "Grams (g)":
			self.molValueOutput2.setPlainText(str(float(self.subGram2.toPlainText()) / Formula(self.formulaInput.toPlainText()).mass))
		else:
			self.molValueOutput2.setPlainText(str((float(self.subGram2.toPlainText())/1000) / Formula(self.formulaInput.toPlainText()).mass))

	# Reverse Solute Mass to Grams of Solute
	def revmos(self):
			if self.soluteWeight2.currentText() == "Grams (g)":
				self.subGram2.setPlainText(str(round((float(self.molValueOutput2.toPlainText()) * Formula(self.formulaInput.toPlainText()).mass) ,6)))
			else:
				self.subGram2.setPlainText(str(round(((float(self.molValueOutput2.toPlainText())*1000) * Formula(self.formulaInput.toPlainText()).mass), 6)))

	# Calculate Molarity
	def molaritybox(self):									
		try:
			if not self.weightCheck.isChecked():
				self.decimal_norm()
				self.M = self.n / self.V
				self.decimal_unnorm()
				self.print_values()
			else:
				self.mos()
				self.decimal_norm()
				self.M = self.n / self.V
				self.decimal_unnorm()
				self.print_values()				
		except ValueError:
			self.recverror()
			self.verror.exec_()
		except ZeroDivisionError:
			self.reczerror()
			self.zerror.exec_()
		except Exception as e:
			self.recferror(e)
			self.ferror.exec_()

	# Calculate Solute Mass
	def solutebox(self):
		try:
			if not self.weightCheck.isChecked():
				self.decimal_norm()
				self.n = self.M * self.V
				self.decimal_unnorm()
				self.print_values()
				self.revmos()
			else:
				self.mos()
				self.decimal_norm()
				self.n = self.M * self.V
				self.decimal_unnorm()
				self.print_values()
				self.revmos()			
		except ValueError:
			self.recverror()
			self.verror.exec_()
		except ZeroDivisionError:
			self.reczerror()
			self.zerror.exec_()
		except Exception as e:
			self.recferror(e)
			self.ferror.exec_()

	# Calculate Volume
	def volbox(self):
		try:
			if not self.weightCheck.isChecked():
				self.decimal_norm()
				self.V = self.n / self.M
				self.decimal_unnorm()
				self.print_values()
			else:
				self.mos()
				self.decimal_norm()
				self.V = self.n / self.M
				self.decimal_unnorm()
				self.print_values()			
		except ValueError:
			self.recverror()
			self.verror.exec_()
		except ZeroDivisionError:
			self.reczerror()
			self.zerror.exec_()
		except Exception as e:
			self.recferror(e)
			self.ferror.exec_()

	#***********************************************************************************************************************
	# Dilution Calculator Tab 4***********************************************************************************************

	# Calculate Molraity M2
	def molbox2(self):
		self.checkVol1()
		try:
			self.decimal_norm2()	
			if self.V2 < self.V1:
				self.v2lowerError()
				self.v2v1error.exec_()
			else:
				self.M2 = (self.M1 * self.V1)/self.V2
				if self.V2 > self.V1:
					self.printAddDil()
				self.decimal_unnorm2()
				self.print_values2()
		except ValueError:
			self.recverror()
			self.verror.exec_()
			self.clear_tab_4()
			self.clearAdds()
		except ZeroDivisionError:
			self.reczerror()
			self.zerror.exec_()
			self.clear_tab_4()
			self.clearAdds()
		except Exception as e:
			self.recferror(e)
			self.ferror.exec_()
			self.clear_tab_4()
			self.clearAdds()

	# Calculate Volume V2
	def volbox2(self):
		self.checkVol1()
		try:
			self.decimal_norm2()
			if self.M2 > self.M1:
				if self.formulaInput.toPlainText() == "":
					self.emptyFormula()
					self.emptyForError.exec_()
				else:	
					self.V2 = self.V1
					self.n1 = self.M1 * self.V1
					self.n2 = self.M2 * self.V2
					self.n3 = self.n2 - self.n1
					self.printAddSol()
					self.decimal_unnorm2()
					self.print_values2()
			else:
				self.V2 = (self.M1 * self.V1)/self.M2
				if self.V2 > self.V1:
					self.printAddDil()
				self.decimal_unnorm2()
				self.print_values2()
		except ValueError:
			self.recverror()
			self.verror.exec_()
			self.clear_tab_4()
			self.clearAdds()
		except ZeroDivisionError:
			self.reczerror()
			self.zerror.exec_()
			self.clear_tab_4()
			self.clearAdds()
		except Exception as e:
			self.recferror(e)
			self.ferror.exec_()
			self.clear_tab_4()
			self.clearAdds()

	# Calculate Vol V1
	def volbox1(self):
		try:
			self.decimal_norm2()
			self.V1 = (self.M2 * self.V2) / self.M1
			self.decimal_unnorm2()
			self.print_values2()
		except ValueError:
			self.recverror()
			self.verror.exec_()
		except ZeroDivisionError:
			self.reczerror()
			self.zerror.exec_()
		except Exception as e:
			self.recferror(e)
			self.ferror.exec_()

	# Non Molar Calculation.
	def nonMolarCalc(self):
		try:
			self.decimal_norm2()
			if self.radmol2.isChecked():
				self.M2 = (self.M1 * self.V1)/self.V2
			elif self.radvol1.isChecked():
				self.V1 = (self.M2 * self.V2) / self.M1
			elif self.radvol2.isChecked():
				self.V2 = (self.M1 * self.V1)/self.M2
			self.print_values2()
		except ValueError:
			self.recverror()
			self.verror.exec_()
		except ZeroDivisionError:
			self.reczerror()
			self.zerror.exec_()
		except Exception as e:
			self.recferror(e)
			self.ferror.exec_()

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	ui = Ui()
	app.exec_()

