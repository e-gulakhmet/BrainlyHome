from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QLineEdit
from PyQt5.QtCore import QRect, Qt, pyqtSignal
import logging


class NewRoomMenu(QDialog):
    # Окно, которое должно открываться,
    # когда мы добавляем новую комнату в roomsmenu.
    # Для устанвоки имени для комнаты

    S_new_room = pyqtSignal(str, name="newRoom")

    def __init__(self):
        super().__init__()

        self.logger = logging.getLogger("NEWROOMMENU")

        self.room_info = {"Name": None}

        self.setObjectName("Dialog")
        self.resize(400, 106)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(10, 60, 371, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.new_room_accepted)
        self.buttonBox.rejected.connect(self.reject)

        self.roomLineEdit = QLineEdit()
        self.roomLineEdit.setObjectName("roomLineEdit")
        self.roomLineEdit.textEdited.connect(self.set_name)

        roomEditLay = QHBoxLayout()
        roomEditLay.setContentsMargins(0, 0, 0, 0)
        roomEditLay.setObjectName("roomEditLay")

        roomEditLay.addWidget(self.roomLineEdit)

        self.setLayout(roomEditLay)

        self.show()

    def set_name(self, name):
        self.room_info["Name"] = name
        self.logger.info("Room name is " + name)
    
    def new_room_accepted(self):
        self.logger.info("New room was accepted.")
        self.S_new_room.emit(self.room_info["Name"])
        self.accept()