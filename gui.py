import sys, os, time, psutil
from PyQt5.QtCore import Qt, QProcess, QTimer, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
# from PyQt5 import QtGui, QtCore

class WhatsAppCaller(QWidget):
    def __init__(self, parent = None):
        super(WhatsAppCaller, self).__init__(parent)
        self.pCall = None
        self.setMinimumSize(320,140)
        self.originalPalette = QApplication.palette()
        qss = "src/styles.qss"
        with open(qss,"r") as fh:
            self.setStyleSheet(fh.read())
        self.createMainWindow()
    
    def createMainWindow(self):
        # Contact textbox
        self.contactTB = QLineEdit(self)
        self.contactTB.setPlaceholderText("Insert contact info (name or phone)")
        self.contactTB.setAlignment(Qt.AlignCenter)
        self.contactTB.returnPressed.connect(self.startCall)
        self.contactTB.setAttribute(Qt.WA_MacShowFocusRect, 0)
        # Call and stop buttons
        self.pbt = {"call":"Call contact","stop":"Stop call"}
        self.startButton = QPushButton(self.pbt["call"])
        self.startButton.clicked.connect(self.startCall)
        self.stopButton = QPushButton(self.pbt["stop"])
        self.stopButton.clicked.connect(self.stopCall)
        # Place widgets in window
        self.layout = QGridLayout()
        self.layout.addWidget(self.contactTB,0,0)
        self.layout.addWidget(self.startButton,1,0)
        self.layout.addWidget(self.stopButton,1,0)
        self.stopButton.hide()
        self.setLayout(self.layout)
    
    def startCall(self):
        if self.pCall != None: 
            print("Another call is in progress.")
            return    
        if self.contactTB.text() == "":
            # self.displayError("No contact information entered.")
            print("No contact information entered.")
            return
        print("Starting call")
        self.pCall = QProcess() # Keep a reference to the QProcess (e.g. on self) while it's running.
        self.pCall.finished.connect(self.stopCall)
        self.pCall.start("python3",[os.path.dirname(__file__) + "/src/whatsapp_android_caller.py", self.contactTB.text()])
        # self.layout.removeWidget(self.startButton)
        self.startButton.hide()
        # self.layout.addWidget(self.stopButton,1,0)
        self.stopButton.show()

    def stopCall(self):
        if self.pCall == None: return
        print("Stopping call")
        self.terminateChildren()
        # self.layout.removeWidget(self.stopButton)
        self.stopButton.hide()
        # self.layout.addWidget(self.startButton,1,0)
        self.startButton.show()

    def terminateChildren(self):
        # Get process tree
        current_process = psutil.Process()
        children = current_process.children(recursive=True)
        children.reverse()
        gchildren = [child for child in children if child.pid != self.pCall.pid()]
        # print("Terminating child processes")
        for child in gchildren:
            if psutil.pid_exists(child.pid):
                # print('Terminating child pid {}'.format(child.pid))
                child.terminate()
        # print("Child processes terminated")
        self.pCall.terminate()
        self.pCall = None

    def displayError(self, text):
        self.errorLabel = QLabel(text)
        self.layout.addWidget(self.errorLabel)

    def closeEvent(self, event):
        self.terminateChildren()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    caller = WhatsAppCaller()
    caller.show()
    sys.exit(app.exec_()) 







# app = QApplication(sys.argv)
# qss = "styles.qss"
# with open(qss,"r") as fh:
#     app.setStyleSheet(fh.read())

# window = QWidget()
# window.setWindowTitle("WhatsApp Android Caller")
# # window.setFixedWidth(1000)
# # window.setStyleSheet("background: #202020;")

# grid = QGridLayout()
# window.setLayout(grid)

# # Logo
# # img = QPixmap("img/whatsapp-bot-icon.png")
# # logo = QLabel()
# # logo.setObjectName("WhatsAppLogo")
# # logo.setPixmap(img)
# # logo.setAlignment(QtCore.Qt.AlignCenter)
# # grid.addWidget(logo)

# # Contact text box
# contacttb = QLineEdit("Insert contact info")
# grid.addWidget(contacttb)

# # Push button
# button = QPushButton("Call contact")
# button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
# grid.addWidget(button)

# window.show()
# sys.exit(app.exec())