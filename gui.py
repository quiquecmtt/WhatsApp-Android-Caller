import sys, time, psutil
from PyQt5.QtCore import Qt, QProcess, QTimer, pyqtSignal
from PyQt5.QtWidgets import *
# from PyQt5.QtGui import QPixmap, QCursor
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
        # Call button
        self.pushButton = QPushButton("Call contact")
        self.pushButton.clicked.connect(self.startCall)
        # Place widgets in window
        layout = QGridLayout()
        layout.addWidget(self.contactTB,0,0)
        layout.addWidget(self.pushButton,1,0)
        self.setLayout(layout)

    def startCall(self):
        if self.contactTB.text() == "":
            print("No contact information entered.")
            return
        self.pCall = QProcess() # Keep a reference to the QProcess (e.g. on self) while it's running.
        self.pCall.finished.connect(self.callFinished)
        self.pCall.daemon = True
        self.pCall.start("python3",["src/whatsapp_android_caller.py", self.contactTB.text()])
        self.pushButton.setEnabled(False)

    def callFinished(self):
        self.pushButton.setEnabled(True)
        self.pCall = None
    
    def closeEvent(self, event):
        # Get process tree
        current_process = psutil.Process()
        children = current_process.children(recursive=True)
        children.reverse()
        print("Terminating child processes")
        for child in children:
            if psutil.pid_exists(child.pid):
                print('Terminating child pid {}'.format(child.pid))
                child.terminate()
        print("Child processes terminated")
        event.accept()


if __name__ == '__main__':

    import sys

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