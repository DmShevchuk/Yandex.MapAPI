import pygame
import requests
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import sys


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(688, 183)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(30, 10, 520, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(550, 8, 121, 34))
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(550, 140, 121, 31))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit2 = QtWidgets.QLineEdit(Form)
        self.lineEdit2.setGeometry(QtCore.QRect(30, 100, 650, 31))
        self.lineEdit2.setFont(font)
        self.lineEdit2.setText("")
        self.lineEdit2.setObjectName("lineEdit")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(30, 50, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Искать"))
        self.pushButton_2.setText(_translate("Form", "Сброс"))
        self.comboBox.setItemText(0, _translate("Form", "Без почтового индекса"))
        self.comboBox.setItemText(1, _translate("Form", "С почтовым индексом"))


class MyWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.clean)
        self.comboBox.currentTextChanged.connect(self.change_postal_index)

    def search(self):
        global longitude, lattitude, pt, pt_coord
        self.current_address = self.lineEdit.text()
        request = 'https://geocode-maps.yandex.ru/1.x/?format=json' \
            f'&apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={self.current_address}&results=1'
        response = requests.get(request)
        try:
            json_response = response.json()
            self.lineEdit2.setText(json_response['response']['GeoObjectCollection']
                                   ['featureMember'][0]['GeoObject']['metaDataProperty']
                                   ['GeocoderMetaData']['AddressDetails']['Country']['AddressLine'])

            self.postal_code = json_response['response']['GeoObjectCollection']['featureMember'][0]\
            ['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']

            position = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']

            longitude = float(position.split()[0])
            lattitude = float(position.split()[1])
            pt = True
            pt_coord = longitude, lattitude

        except Exception:
            self.lineEdit2.setText('Что-то пошло не так(')

    def change_postal_index(self):
        if self.comboBox.currentText() == 'С почтовым индексом':
            self.lineEdit2.setText(self.lineEdit2.text() + ', ' + self.postal_code)
        else:
            self.lineEdit2.setText(self.lineEdit2.text()[:-7])

    def clean(self):
        global pt
        self.lineEdit.setText('')
        self.lineEdit2.setText('')
        self.comboBox.setCurrentIndex(0)
        self.current_address = ''
        self.postal_code = ''
        pt = False



map_request = 'http://static-maps.yandex.ru/1.x/'

longitude = 31.268856
lattitude = 58.523656
delta = 0.002
type_map = 'map'
pt = False
pt_coord = ''
map_params = {
    'll': ','.join([str(longitude), str(lattitude)]),
    "spn": ",".join([str(delta), str(delta)]),
    "l": type_map
}


def map():
    map_params = {
        'll': ','.join([str(longitude), str(lattitude)]),
        "spn": ",".join([str(delta), str(delta)]),
        "l": type_map,
        'pt': ','.join([str(pt_coord[0]), str(pt_coord[1])]) if pt else '',
    }

    response = requests.get(map_request, params=map_params)
    map = 'map.png'
    with open(map, 'wb') as photo:
        photo.write(response.content)
    photo = pygame.image.load(map)
    os.remove(map)
    return photo


pygame.init()

SIZE = [600, 450]
font = pygame.font.Font(None, 20)
screen = pygame.display.set_mode(SIZE)
screen.fill((255, 255, 255))

#Верхнее меню
text = font.render('Схема', 1, (0, 0, 0))
text_x, text_y = 425, 10
screen.blit(text, (text_x, text_y))
text = font.render('Гибрид', 1, (0, 0, 0))
text_x, text_y = 540, 10
screen.blit(text, (text_x, text_y))
text = font.render('Спутник', 1, (0, 0, 0))
text_x, text_y = 475, 10
screen.blit(text, (text_x, text_y))
pygame.draw.rect(screen, (0, 0, 0), (5, 5, 150, 30), 1)
text = font.render('Поиск', 1, (0, 0, 0))
text_x, text_y = 57, 14
screen.blit(text, (text_x, text_y))

#Окно с поиском
app = QApplication(sys.argv)
ex = MyWidget()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 265:
                if delta * 2 <= 66:
                    delta *= 2
            if event.key == 259:
                if delta / 2 >= 0.0005:
                    delta /= 2

            if event.key == pygame.K_UP:
                if lattitude + delta <= 83:
                    lattitude += delta

            if event.key == pygame.K_DOWN:
                if lattitude - delta >= -83:
                    lattitude -= delta

            if event.key == pygame.K_RIGHT:
                if longitude + delta > 180:
                    longitude = -180
                else:
                    longitude += delta

            if event.key == pygame.K_LEFT:
                if longitude - delta < -180:
                    longitude = 180
                else:
                    longitude -= delta
            map()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                if 425 <= x <= 465 and 0 <= y <= 35:
                    type_map = 'map'
                if 475 <= x <= 530 and 0 <= y <= 35:
                    type_map = 'sat'
                if 540 <= x <= 590 and 0 <= y <= 35:
                    type_map = 'sat,skl'
                if 5 <= x <= 155 and 5 <= y <= 35:
                    ex.show()

    screen.blit(map(), (0, 40))
    pygame.display.flip()
