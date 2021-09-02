import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
 
app = QApplication(sys.argv)
qss = "styles.qss"
with open(qss,"r") as fh:
    app.setStyleSheet(fh.read())

window = QWidget()
window.setWindowTitle("WhatsApp Android Caller")
# window.setFixedWidth(1000)
# window.setStyleSheet("background: #202020;")

grid = QGridLayout()
window.setLayout(grid)

# Logo
# img = QPixmap("img/whatsapp-bot-icon.png")
# logo = QLabel()
# logo.setObjectName("WhatsAppLogo")
# logo.setPixmap(img)
# logo.setAlignment(QtCore.Qt.AlignCenter)
# grid.addWidget(logo)

# Contact text box
contacttb = QLineEdit("Insert contact info")
grid.addWidget(contacttb)

# Push button
button = QPushButton("Call contact")
button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
grid.addWidget(button)

window.show()
sys.exit(app.exec())