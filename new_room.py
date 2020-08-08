# Окно, которое должно открываться,
# когда мы добавляем новую комнату в roomsmenu.



from PyQt5.QtWidgets import QDialog, QWidget, QDialogButtonBox, QHBoxLayout, QLineEdit
from PyQt5.QtCore import QRect, Qt, pyqtSignal


class NewRoomMenu(QDialog):

    S_new_room = pyqtSignal(str, name="newRoom")

    def __init__(self):

        self.room_info = {"Name": None}

        super().__init__()
        self.setObjectName("Dialog")
        self.resize(400, 106)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(10, 60, 371, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.new_room_accepted)
        self.buttonBox.rejected.connect(self.reject)

        self.hLay = QWidget(self)
        self.hLay.setGeometry(QRect(0, 9, 391, 41))
        self.hLay.setObjectName("hLay")

        self.roomLineEdit = QLineEdit(self.hLay)
        self.roomLineEdit.setObjectName("roomLineEdit")
        self.roomLineEdit.textChanged.connect(self.set_name)

        self.roomEditLay = QHBoxLayout(self.hLay)
        self.roomEditLay.setContentsMargins(0, 0, 0, 0)
        self.roomEditLay.setObjectName("roomEditLay")

        self.roomEditLay.addWidget(self.roomLineEdit)

    def set_name(self, name):
        self.room_info["Name"] = name
    
    def new_room_accepted(self):
        self.S_new_room.emit(self.room_info["Name"])
        self.accept()