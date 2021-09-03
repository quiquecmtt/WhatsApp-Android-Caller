import sys
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import *
# from PyQt5.QtGui import QPixmap, QCursor
# from PyQt5 import QtGui, QtCore


class WhatsAppCaller(QDialog):
    def __init__(self, parent = None):
        super(WhatsAppCaller, self).__init__(parent)
        self.setMinimumSize(320,140)
        self.originalPalette = QApplication.palette()
        qss = "styles.qss"
        with open(qss,"r") as fh:
            self.setStyleSheet(fh.read())
        self.createMainWindow()
    
    def createMainWindow(self):
        # Contact textbox
        self.contactTB = QLineEdit(self)
        self.contactTB.setPlaceholderText("Insert contact info (name or phone)")
        self.contactTB.setAlignment(Qt.AlignCenter)
        # Call button
        pushButton = QPushButton("Call contact")
        pushButton.clicked.connect(self.buttonClicked)
        # Place widgets in window
        layout = QGridLayout()
        layout.addWidget(self.contactTB)
        layout.addWidget(pushButton)
        self.setLayout(layout)

    def buttonClicked(self):
        print("Button was pushed")

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