from PyQt5.QtWidgets import QWidget, QSizePolicy, QLabel, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QLayout
from PyQt5.QtWidgets import QComboBox, QScrollArea, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, QRect, Qt, QTimer
import logging

import home
import connection



class ClientWidget(QFrame):
    def __init__(self, client: home.Client):
        super().__init__()

        self.client = client

        self.setObjectName("ClientWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setSizePolicy(sizePolicy)
        self.setStyleSheet("QPushButton{\n"
                           "    width: 60px;\n"
                           "    height: 60px;\n"
                           "}")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        
        # Информация о клиенте
        self.nameLineEdit = QLineEdit(self)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.nameLineEdit.setText(self.client.get_name())

        self.typeLabel = QLabel(self)
        self.typeLabel.setObjectName("typeLabel")
        self.typeLabel.setText(self.client.get_kind())

        self.idLabel = QLabel(self)
        self.idLabel.setObjectName("idLabel")
        self.idLabel.setText(self.client.get_id())
        
        # Проствранство с информацией о клиенте
        infoVLay = QVBoxLayout()
        infoVLay.setContentsMargins(0, -1, -1, -1)
        infoVLay.setObjectName("infoVLay")

        infoVLay.addWidget(self.nameLineEdit)
        infoVLay.addWidget(self.typeLabel)
        infoVLay.addWidget(self.idLabel)

        line = QFrame(self)
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setObjectName("line")

        line_2 = QFrame(self)
        line_2.setFrameShape(QFrame.VLine)
        line_2.setFrameShadow(QFrame.Sunken)
        line_2.setObjectName("line_2")

        # Кнопка открытия настроек клиента
        self.infoButton = QPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.infoButton.sizePolicy().hasHeightForWidth())
        self.infoButton.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addPixmap(QPixmap("../../../../../Downloads/right-arrows.png"), QIcon.Normal, QIcon.Off)
        self.infoButton.setIcon(icon)
        self.infoButton.setIconSize(QSize(60, 60))
        self.infoButton.setObjectName("infoButton")


        # Основное пространство
        self.clientHLay = QHBoxLayout()
        self.clientHLay.setObjectName("clientHLay")

        self.clientHLay.addLayout(infoVLay)
        self.clientHLay.addWidget(line)
        self.clientHLay.addStretch()
        self.clientHLay.addWidget(line_2)
        self.clientHLay.addWidget(self.infoButton)

        self.setLayout(self.clientHLay)

        self.show()



class RoomsMenu(QWidget):
    def __init__(self, mqtt):
        super().__init__()

        self.rooms = [home.Room("All"), home.Room("MyRoom")]

        self.logger = logging.getLogger("ROOMSMENU")

        # Подключаемся к помошнику с дополнительными функциями для mqtt
        self.mqtt_helper = connection.MqttHelper(mqtt)

        self.setObjectName("RoomsWidget")

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.setStyleSheet("QLabel{\n"
                           "    font-size: 16px;\n"
                           "}\n"
                           "QLabel#mainLabel{\n"
                           "    font-size: 25px;\n"
                           "}\n"
                           "QComboBox{\n"
                           "    font-size: 20px\n"
                           "}\n"
                           "QLineEdit{\n"
                           "    font-size: 20px;\n"
                           "}\n"
                           "QPushButton{\n"
                           "    width: 70px;\n"
                           "    height: 70px;\n"
                           "    margin-right: 5px;\n"
                           "}\n"
                           "QFrame#clientFrame{\n"
                           "    border: 1px solid;\n"
                           "}")

        # Название окна
        mainLabel = QLabel(self)
        mainLabel.setFrameShape(QFrame.NoFrame)
        mainLabel.setScaledContents(False)
        mainLabel.setObjectName("mainLabel")
        mainLabel.setText("Rooms")

        # Пространство для объекта название окна
        labelHLay = QHBoxLayout()
        labelHLay.setSizeConstraint(QLayout.SetMinimumSize)
        labelHLay.setObjectName("labelHLay")
        labelHLay.addStretch()
        labelHLay.addWidget(mainLabel)
        labelHLay.addStretch()

        # Прямая разделяющая заголовок окна и меню комнат
        line = QFrame(self)
        line.setLineWidth(1)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setObjectName("line")

        # Список комнат с возможностью выбора комнаты
        self.RoomsBox = QComboBox(self)
        self.RoomsBox.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.RoomsBox.setSizePolicy(sizePolicy)
        self.RoomsBox.setMaximumSize(QSize(200, 100))
        self.RoomsBox.setObjectName("RoomsBox")
        for room in self.rooms:
            self.RoomsBox.addItem(room.get_name())
        self.RoomsBox.currentIndexChanged.connect(self.update_room)

        # Простаранство для объекта выбора комнат
        RoomsLayout = QHBoxLayout()
        RoomsLayout.setObjectName("RoomsLayout")
        RoomsLayout.addWidget(self.RoomsBox)

        # Пространство клиентов и возможностью прокрутки
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 764, 691))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.scrollAreaLayout.setObjectName("scrollAreaLayout")

        self.RoomScrollArea = QScrollArea(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.RoomScrollArea.setSizePolicy(sizePolicy)
        self.RoomScrollArea.setMinimumSize(QSize(0, 100))
        self.RoomScrollArea.setMouseTracking(True)
        self.RoomScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.RoomScrollArea.setWidgetResizable(True)
        self.RoomScrollArea.setObjectName("RoomScrollArea")
        self.RoomScrollArea.setWidget(self.scrollAreaWidgetContents_2)

        # Основоное простанство для всех остальных простанств
        self.mainVLay = QVBoxLayout()
        self.mainVLay.setSizeConstraint(QLayout.SetMaximumSize)
        self.mainVLay.setObjectName("mainVLay")
        self.mainVLay.addLayout(labelHLay)
        self.mainVLay.addWidget(line)
        self.mainVLay.addLayout(RoomsLayout)
        self.mainVLay.addWidget(self.RoomScrollArea)

        self.setLayout(self.mainVLay)
        
        self.show()

        timer = QTimer(self)
        timer.setInterval(5000)
        timer.setSingleShot(False)
        # timer.timeout.connect(self.update_rooms)
        timer.start(5000)


    
    def delete_room(self, room): # Удалить комнату по имени
        try:
            self.RoomsBox.removeItem(self.rooms.index(room))
            self.rooms.remove(room)
            self.logger.info("Room [" + room.get_name() + "] was deleted")
        except ValueError:
            self.logger.warning(room.get_name() + " is missing from the list of rooms")
    
    def add_room(self, room): # Добавить комнату
        self.rooms.append(room)
        self.logging.info("Room [" + room.get_name() + "] was added")

    def update_room(self, index): # Обновить окно комнат
        if index == 0: # Если выбрана комната со всеми клиентами
            # Ищем новых клиентов
            self.rooms[0].add_clients(self.mqtt_helper.get_devices()) 

        # Удаляем всех клиентов из виджета комнаты,
        # чтобы потом загрузить клиентов из выбранной комнаты
        layout = self.scrollAreaWidgetContents_2.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Добавляем клиентов из выбранной комнаты в виджет комнаты
        for c in self.rooms[index].get_clients():
            self.scrollAreaLayout.addWidget(ClientWidget(c))
        
        self.scrollAreaLayout.addStretch(1)