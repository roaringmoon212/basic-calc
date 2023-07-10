#Code Project ??? : Building a Simple Calculator using MVC design

##This is the script for the GUI behind a simple calculator, built to test PyQt6 and its functionality.

'''
import sys
from PyQt6.QtWidgets import QApplication, QLabel, QLayout, QWidget

###Create an instance of QApplication
app = QApplication([])

###Create a basic window with a label
window = QWidget()
window.setWindowTitle("PyQt Calculator")
window.setGeometry(100, 100, 280, 80)
helloMsg = QLabel("<h1>Hello, World!</h1>", parent=window)
helloMsg.move(60,15)

###Show the GUI
window.show()

###Run the application's event loop
sys.exit(app.exec())
'''

###Building the actual calculator:
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QGridLayout, QLineEdit, QMainWindow,
                           QPushButton, QVBoxLayout, QWidget)
from functools import partial

WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40
ERROR_MSG = 'Error!'

###Boilerplate (base) code:
class PyCalcWindow(QMainWindow):
    '''Main window for the app'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyCalc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

###Front-end development:
class PyCalcWindow(QMainWindow):
    '''Main window for the app'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyCalc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QGridLayout()
        keyBoard = [
            ['7', '8', '9', '/', 'C'],
            ['4', '5', '6', '*', '('],
            ['1', '2', '3', '-', ')'],
            ['0', '00', '.', '+', '='],
        ]
        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)
        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        '''Set display's text'''
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        '''Get display text'''
        return self.display.text()

    def clearDisplay(self):
        '''Clear the display'''
        self.setDisplayText()

def evaluateExpression(expression):
    '''Evaluate an expression (model)'''
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result

class PyCalc:
    '''PyCalc's controller class'''
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()

    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, subExpression):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + subExpression
        self._view.setDisplayText(expression)

    def _connectSignalsAndSlots(self):
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {'=', 'C'}:
                button.clicked.connect(
                    partial(self._buildExpression, keySymbol)
                )
        self._view.buttonMap["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)

def main():
    '''Main function for the app'''
    pycalcApp = QApplication([])
    pycalcWindow = PyCalcWindow()
    pycalcWindow.show()
    PyCalc(model=evaluateExpression, view=pycalcWindow)
    sys.exit(pycalcApp.exec())

if __name__ == "__main__":
    main()
