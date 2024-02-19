import sys
import os
import configparser
import webbrowser
import ast
import sqlite3
import threading
import time

from PyQt6 import QtWidgets, QtCore, QtNetwork
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtGui import QFont, QFontDatabase, QPalette, QIcon, QAction, QColor, QPixmap, QCursor
# from PyQt6.QtCore import QSize, Qt, QPoint, QUrl
from PyQt6.QtWidgets import (QMainWindow, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
    QVBoxLayout, QWidget, QFrame, QMessageBox, QFileDialog, QGraphicsEffect)

from sqlite3 import Error
from add import EquipmentAdd
from change import EquipmentChange
from weather import WeatherGet

path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])

characteristics__to = {'id': 'id', 'id__room': 'Помещения', 'id__transformer': 'Трансформатор',
                       'id__shield': 'Щит', 'name': 'Наименование', 'manufacturer': 'Производитель',
                       'power': 'Мощьность', 'nominal__voltage': 'Напряжение',
                       'nominal__current': 'Ток', 'nominal__speed': 'Скорость',
                       'weight': 'Вес', 'size': 'Размер ВхШхГ', 'international__protection': 'Класс защиты',
                       'efficiency': 'КПД', 'motor__starting_method': 'Метод запуска двигателя',
                       'connection__diagram': 'Диаграмма соединения', 'id__auto_switch': 'Номер автомата',
                       'electrical__safety_class': 'Класс помещения', 'mounting__type': 'Способ монтажа',
                       'number__posts': 'Количество постов', 'material__shield': 'Материал щита',
                       'pin__count': 'Количество контактов', 'voltage': 'Напряжение',
                       'maximal__current': 'Максимальный ток', 'number__keys': 'Количество клавиш',
                       'floor': 'Этаж', 'zone': 'Зона', 'lamp__type': 'Тип лампы', 'length': 'Длинна',
                       'cross__section': 'Сечение', 'number__of_cores': 'Количество жил', 'material': 'Материал',
                       'mark': 'Марка', 'leakage__current': 'Ток утечки', 'cutoff__current': 'Ток',
                       'characteristic': 'Характеристика', 'type': 'Тип',
                       'nominal__voltage_out': 'Номинальное напряжение на выходе',
                       'nominal__voltage_in': 'Номинальное напряжение на входе', 'lamp__quantity': 'Количество ламп'}


equipment__type = {'air__curtain': 'Воздушная завеса', 'auto__switch': 'Автоматические выключатели',
                   'cable': 'Кабели', 'conditioner': 'Кондиционеры', 'electric__motor': 'Электромоторы',
                   'lighting': 'Освещение', 'rooms': 'Помещения', 'shield': 'Щиты', 'sockets': 'Розетки',
                   'switch': 'Выключатели', 'transformer': 'Трансформатор'}

def create__table(connection, cur):
    transformer = ("""CREATE TABLE if not exists "transformer" (
                                    "id__transformer"	TEXT,
	                                "manufacturer"	TEXT,
	                                "nominal__voltage_in"	INTEGER,
	                                "nominal__voltage_out"	INTEGER,
	                                "nominal__current"	INTEGER,
	                                "power"	INTEGER,
	                                "weight"	REAL,
	                                "size"	TEXT,
	                                "id__room"	TEXT,
	                                PRIMARY KEY("id__transformer")
                                    )""")
    air__curtain = ("""CREATE TABLE if not exists "air__curtain" (
                                    "id"	INTEGER,
                                    "name"	TEXT,
	                                "manufacturer"	TEXT,
	                                "power"	INTEGER,
	                                "nominal__voltage"	INTEGER,
	                                "nominal__current"	INTEGER,
	                                "weight"	REAL,
	                                "size"	TEXT,
	                                "id__shield"	TEXT,
	                                "id__auto_switch"	INTEGER,
	                                "id__room"	TEXT,
	                                PRIMARY KEY("id" AUTOINCREMENT)
                                    )""")
    auto__switch = ("""CREATE TABLE if not exists "auto__switch" (
	                        "id"	INTEGER,
	                        "name"	TEXT,
	                        "manufacturer"	TEXT,
	                        "type"	TEXT,
	                        "size"	TEXT,
	                        "characteristic"	TEXT,
	                        "cutoff__current"	INTEGER,
	                        "leakage__current"	INTEGER,
	                        "id__shield"	TEXT,
	                        "id__auto_switch"	INTEGER,
	                        PRIMARY KEY("id" AUTOINCREMENT)
                            )""")
    cable = ("""CREATE TABLE if not exists "cable" (
	                "id"	INTEGER,
	                "name"	TEXT,
	                "manufacturer"	TEXT,
	                "mark"	TEXT,
	                "material"	TEXT,
	                "number__of_cores"	INTEGER,
	                "cross__section"	REAL,
	                "length"	INTEGER,
	                "id__shield"	TEXT,
	                "id__auto_switch"	INTEGER,
	                PRIMARY KEY("id" AUTOINCREMENT)
                    )""")
    conditioner = ("""CREATE TABLE if not exists "conditioner" (
	                        "id"	INTEGER,
	                        "name"	TEXT,
	                        "manufacturer"	TEXT,
	                        "power"	INTEGER,
	                        "nominal__voltage"	INTEGER,
	                        "nominal__current"	INTEGER,
	                        "weight"	REAL,
	                        "size"	TEXT,
	                        "id__shield"	TEXT,
	                        "id__auto_switch"	INTEGER,
	                        "id__room"	TEXT,
	                        PRIMARY KEY("id" AUTOINCREMENT)
                            )""")
    electric__motor = ("""CREATE TABLE if not exists "electric__motor" (
	                        "id"	INTEGER,
	                        "name"	TEXT,
	                        "manufacturer"	TEXT,
	                        "power"	INTEGER,
	                        "nominal__voltage"	INTEGER,
	                        "nominal__current"	REAL,
	                        "nominal__speed"	INTEGER,
	                        "weight"	REAL,
	                        "size"	TEXT,
	                        "efficiency"	INTEGER,
	                        "motor__starting_method"	TEXT,
	                        "international__protection"	INTEGER,
	                        "id__shield"	TEXT,
	                        "id__auto_switch"	INTEGER NOT NULL,
	                        "id__room"	TEXT,
	                        PRIMARY KEY("id" AUTOINCREMENT)
                            )""")
    lighting = ("""CREATE TABLE if not exists "lighting" (
	                    "id"	INTEGER,
	                    "name"	TEXT,
	                    "manufacturer"	TEXT,
	                    "mounting__type"	TEXT,
	                    "international__protection"	INTEGER,
	                    "lamp__type"	TEXT,
	                    "lamp__quantity"    TEXT,
	                    "voltage"	INTEGER,
	                    "power"	INTEGER,
	                    "id__shield"	TEXT,
	                    "id__auto_switch"	INTEGER NOT NULL,
	                    "id__room"	TEXT NOT NULL,
	                    PRIMARY KEY("id" AUTOINCREMENT)
                        )""")
    rooms = ("""CREATE TABLE if not exists "rooms" (
	                "id__room"	TEXT UNIQUE,
	                "zone"	TEXT,
	                "floor"	TEXT,
	                "electrical__safety_class"	TEXT,
	                PRIMARY KEY("id__room")
                    )""")
    shield = ("""CREATE TABLE if not exists "shield" (
	                "id__shield"	TEXT NOT NULL,
	                "manufacturer"	TEXT,
	                "mounting__type"	TEXT,
	                "number__posts"	INTEGER,
	                "size"	TEXT,
	                "material__shield"	TEXT,
	                "international__protection"	INTEGER,
	                "id__room"	TEXT,
	                PRIMARY KEY("id__shield")
                    )""")
    sockets = ("""CREATE TABLE if not exists "sockets" (
	                "id"	INTEGER,
	                "name"	TEXT,
	                "manufacturer"	TEXT,
	                "mounting__type"	TEXT,
	                "pin__count"	INTEGER,
	                "international__protection"	INTEGER,
	                "voltage"	INTEGER,
	                "maximal__current"	INTEGER,
	                "id__shield"	TEXT,
	                "id__auto_switch"	INTEGER NOT NULL,
	                "id__room"	TEXT,
	                PRIMARY KEY("id" AUTOINCREMENT)
                    )""")
    switch = ("""CREATE TABLE if not exists "switch" (
	                "id"	INTEGER,
	                "name"	TEXT,
	                "manufacturer"	TEXT,
	                "mounting__type"	TEXT,
	                "number__keys"	INTEGER,
	                "international__protection"	INTEGER,
	                "voltage"	INTEGER,
	                "maximal__current"	INTEGER,
	                "id__shield"	TEXT,
	                "id__auto_switch"	INTEGER NOT NULL,
	                "id__room"	TEXT,
	                PRIMARY KEY("id" AUTOINCREMENT)
                    )""")
    try:
        cur.execute(air__curtain)
        cur.execute(auto__switch)
        cur.execute(cable)
        cur.execute(conditioner)
        cur.execute(electric__motor)
        cur.execute(lighting)
        cur.execute(rooms)
        cur.execute(shield)
        cur.execute(sockets)
        cur.execute(switch)
        cur.execute(transformer)
        connection.commit()
    except sqlite3.Error as err:
        print(err)


def create__connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        # print("Connection to SQLite DB successful")
        cur = connection.cursor()
        create__table(connection, cur)  # Надо сделать проверку создания таблиц только если их нет в базе
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=None)
        global path
        self.path = path
        # загружаем настройки
        self.path__db = self.load__settings("db")
        # --------------------

        # title bar customize
        btn__title_size = 30
        self.frame__bar = QFrame(self)
        self.frame__bar.setObjectName("frame__title_bar")
        self.frame__bar.setFixedSize(730, 30)
        self.frame__bar_layout = QHBoxLayout(spacing = 0)
        self.frame__bar_layout.setContentsMargins(0, 0, 0, 0)

        self.title__name = QLabel("Редактор оборудования")
        self.title__name.setObjectName("title__name")
        # pixmap = QPixmap('./icon/tools.svg')
        # self.title__name.setPixmap(pixmap)

        self.btn__exit = QPushButton("x")
        self.btn__exit.setObjectName("exit")
        self.btn__exit.setFixedSize(btn__title_size, btn__title_size)
        self.btn__exit.clicked.connect(self.btn__close_clicked)
        self.btn__min = QPushButton("_")
        self.btn__min.setObjectName("min")
        self.btn__min.setFixedSize(btn__title_size, btn__title_size)
        self.btn__min.clicked.connect(self.btn__min_clicked)
        self.btn__open = QPushButton()
        self.btn__open = QPushButton("+")
        self.btn__open.setObjectName("open")
        self.btn__open.setFixedSize(btn__title_size, btn__title_size)
        self.btn__open.clicked.connect(self.open__file)

        self.frame__bar_layout.addWidget(self.btn__open)
        self.frame__bar_layout.addStretch(1)
        self.frame__bar_layout.addWidget(self.title__name)
        self.frame__bar_layout.addStretch(1)
        self.frame__bar_layout.addWidget(self.btn__min)
        self.frame__bar_layout.addWidget(self.btn__exit)
        self.frame__bar.setLayout(self.frame__bar_layout)
        self.frame__bar.mouseMoveEvent = self.move__app
        #---------------end title bar customize-------------

        self.statusBar().setStyleSheet("background: transparent")
        self.statusbar__btn_setings = QPushButton()
        self.statusbar__btn_setings.clicked.connect(self.weather__change_settings)
        self.statusbar__btn_setings.setStyleSheet(f"border: none; "
                                                  f"padding: 0; width: 24px; height: 24px;"
                                                  f"background-image: url({self.path}/icon/weather/icons8-settings-24.png);"
                                                  f"background-repeat: no-repeat;")
        self.statusbar__btn_setings.setContentsMargins(0, 0, 0, 0)
        self.statusbar__temp = QLabel("...  ")
        self.statusbar__wind = QLabel("...  ")
        self.statusbar__humidity = QLabel("...  ")
        self.statusBar().setStyleSheet('QStatusBar::item {border: None;}')
        self.statusBar().addPermanentWidget(self.statusbar__temp, stretch=0)
        self.statusBar().addPermanentWidget(self.statusbar__wind, stretch=0)
        self.statusBar().addPermanentWidget(self.statusbar__humidity, stretch=0)
        self.statusBar().addPermanentWidget(self.statusbar__btn_setings, stretch=0)
        self.setObjectName("MainWindow")
        self.setWindowTitle("Редактор оборудования")
        self.setFixedSize(730, 490)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        # -----------db connect

        if os.path.isfile(self.path__db):
            self.sqlite__connect = sqlite3.connect(f"{self.path__db}")
        else:
            self.sqlite__connect = create__connection('equipment.db')
            # path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
            # path__db_new = os.path.abspath('equipment.db')
            config__write_path_data = configparser.ConfigParser()
            config__write_path_data.read(f"{self.path}/settings.ini")
            config__write_path_data.set("path__database", "path", f"{self.path}")
            with open(f'{self.path}/settings.ini', 'w') as configfile:
                config__write_path_data.write(configfile)

        self.sqlite__cursor = self.sqlite__connect.cursor()
        # db connect-------------

        self.windowUI()

        self.sizeX = QApplication.primaryScreen().geometry().width()
        self.sizeY = QApplication.primaryScreen().geometry().height()
        self.app__sizeX = self.width()
        self.app__sizeY = self.height()
        self.biasX = int(self.sizeX / 2 - int(self.app__sizeX / 2))
        self.biasY = int(self.sizeY / 2 - int(self.app__sizeY / 2))
        self.move(self.biasX, self.biasY)
        # path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
        with open(f"{self.path}/qss/dark.css", "r") as f:
            _style = f.read()
            app.setStyleSheet(_style)
        self.weatherget__create()
        threading.Thread(target=self.timer__start, daemon=True).start()

    def weatherget__create(self):
        settings__read = configparser.ConfigParser()
        settings__read.read(f"{self.path}/settings.ini", encoding="utf-8")
        self.url = settings__read["weather"]["url"]
        self.city = settings__read["weather"]["city"]
        self.param = settings__read["weather"]["param"]
        self.token = settings__read["weather"]["token"]
        self.interval = int(settings__read["weather"]["interval"])
        # print(threading.current_thread())
        self.get = WeatherGet(self.url, self.city, self.param, self.token)

    def timer__start(self):
        while True:
            # print(threading.current_thread())
            self.res = ''
            self.res = self.get.get__temp_api()
            if self.res != 400 and self.res != 401 and self.res != 403 and self.res != 404 and self.res != 429:
                self.statusbar__temp.setText(f"Температура: {self.res['main']['temp']}C  ")
                self.statusbar__wind.setText(f"Ветер: {self.res['wind']['speed']}м/с  ")
                self.statusbar__humidity.setText(f"Влажность: {self.res['main']['humidity']}%  ")
            else:
                self.statusbar__temp.setText("...")
                self.statusbar__wind.setText("...")
                self.statusbar__humidity.setText(f"Ошибка {self.res}")
            time.sleep(self.interval)
        # threading.Timer(self.interval, self.timer__start, args=None, kwargs=None).start()
        # print(threading.current_thread())

    def weather__change_settings(self):
        settings__read = configparser.ConfigParser()
        settings__read.read(f"{self.path}/settings.ini", encoding="utf-8")
        city = settings__read["weather"]["city"]
        token = settings__read["weather"]["token"]

        self.weather__settings_window = QDialog()
        self.weather__settings_window.setModal(True)
        self.weather__settings_window.setStyleSheet("border-radius: 5px")
        self.weather__settings_window.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.weather__settings_window.resize(400, 100)
        self.weather__label_city = QLabel("Город")
        self.weather__label_token = QLabel("Ваш ключ")
        self.weather__input_city = QLineEdit(f"{city}")
        self.weather__input_token = QLineEdit(f"{token}")
        self.weather__btn_save = QPushButton("Сохранить")
        self.weather__btn_save.clicked.connect(lambda: self.weather__save(self.weather__input_city.text(),
                                                                          self.weather__input_token.text()))
        self.weather__btn_close = QPushButton("Закрыть")
        self.weather__btn_close.clicked.connect(lambda: self.weather__settings_window.accept())
        self.layout__box = QFormLayout()
        self.layout__box.addRow(self.weather__label_city, self.weather__input_city)
        self.layout__box.addRow(self.weather__label_token, self.weather__input_token)
        self.layout__btn = QHBoxLayout()
        # self.weather__link_reg = QLabel("openweathermap.org")
        # self.weather__link_reg.setStyleSheet("color: rgb(214,214,214);")
        self.weather__link_reg = QPushButton("OpenWeather")
        self.weather__link_reg.setObjectName("weather__link_reg")
        self.weather__link_reg.clicked.connect(lambda: webbrowser.open("https://home.openweathermap.org/users/sign_up"))
        self.weather__link_reg.setStyleSheet("#weather__link_reg{border: none; background: rgb(36, 37, 42);}"
                                             "#weather__link_reg:hover{color:blue}")
        self.layout__btn.addWidget(self.weather__link_reg)
        self.layout__btn.addWidget(self.weather__btn_save)
        self.layout__btn.addWidget(self.weather__btn_close)
        self.layout__box.addRow(self.layout__btn)
        self.weather__settings_window.setLayout(self.layout__box)
        self.weather__settings_window.show()

    def weather__save(self, city, token):
        c = city
        t = token
        settings = configparser.ConfigParser()
        settings.read(f"{self.path}/settings.ini")
        settings.set("weather", "city", f"{c}")
        settings.set("weather", "token", f"{t}")
        with open(f'{self.path}/settings.ini', 'w', encoding="utf-8") as configfile:
            settings.write(configfile)
        self.weather__settings_window.accept()
        self.city = c
        self.token = t
        self.get.set__city(c)
        self.get.set__token(t)
        self.get__temp()

    def handleResponse(self, reply):
        er = reply.error()
        if er == QtNetwork.QNetworkReply.NetworkError.NoError:
            self.res = ast.literal_eval(str(reply.readAll(), 'utf-8'))
            self.statusbar__temp.setText(f"Температура: {self.res['main']['temp']} C")
            self.statusbar__wind.setText(f"Ветер: {self.res['wind']['speed']} м/с")
            self.statusbar__humidity.setText(f"Влажность: {self.res['main']['humidity']} %")
        else:
            self.statusbar__temp.setText("...")
            self.statusbar__wind.setText("...")
            self.statusbar__humidity.setText(f"Ошибка {er} ")
            # print("Error occurred: ", er)
            # print(reply.errorString())

    def get__temp(self):
        url = self.url + f"q={self.city}" + self.param + f"&appid={self.token}"
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        self.manager = QtNetwork.QNetworkAccessManager()
        self.manager.finished.connect(self.handleResponse)
        self.manager.get(request)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def move__app(self, event):
      self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
      self.dragPos = event.globalPosition().toPoint()
      event.accept()

    def btn__close_clicked(self):
        # self.weather.cancel()
        self.close()

    def btn__min_clicked(self):
        self.showMinimized()

    def additionally__equip_info(self):
        table__name = self.sender().objectName()
        loc = self.equipment__location_qcombobox.currentText()
        table__colum_name = self.sqlite__cursor.execute(f"pragma table_info({table__name})").fetchall()
        table__col = []
        name_col = []
        for n in table__colum_name:
            if n[1] == "id":
                continue
            elif n[1] == "id__auto_switch" and table__name == "auto__switch":
                name_col.append("Запитан от")
            elif n[1] == "id__shield" and table__name == "auto__switch":
                name_col.append("Расположен")
            else:
                name_col.append(characteristics__to[n[1]])

        select__value_lighting = 'name, manufacturer, mounting__type, international__protection, lamp__type, \
                            lamp__quantity, voltage, power, id__shield, \
                            (SELECT name FROM auto__switch WHERE auto__switch.id=lighting.id__auto_switch), id__room'
        select__value_air_curtain = 'name, manufacturer, power, nominal__voltage, nominal__current, weight, size, \
            id__shield, (SELECT name FROM auto__switch WHERE auto__switch.id=air__curtain.id__auto_switch), id__room'
        select__value_conditioner = 'name, manufacturer, power, nominal__voltage, nominal__current, weight, size, \
            id__shield, (SELECT name FROM auto__switch WHERE auto__switch.id=conditioner.id__auto_switch), id__room'
        select__value_electric_motor = 'name, manufacturer, power, nominal__voltage, nominal__current, nominal__speed, \
            weight, size, efficiency, motor__starting_method, international__protection, id__shield, \
            (SELECT name FROM auto__switch WHERE auto__switch.id=electric__motor.id__auto_switch), id__room'
        select__value_sockets = 'name, manufacturer, mounting__type, pin__count, international__protection, voltage, \
            maximal__current, id__shield, \
            (SELECT name FROM auto__switch WHERE auto__switch.id=sockets.id__auto_switch), id__room'
        select__value_switch = 'name, manufacturer, mounting__type, number__keys, international__protection, \
            voltage, maximal__current, id__shield, \
            (SELECT name FROM auto__switch WHERE auto__switch.id=switch.id__auto_switch), id__room'
        select__value_shield = 'id__shield, manufacturer, mounting__type, number__posts, size, material__shield, \
                                international__protection, id__room'
        select__value_transformer = 'id__transformer, manufacturer, nominal__voltage_in, nominal__voltage_out, \
            nominal__current, power, weight, size, id__room'

        for name in table__colum_name:
            if name[1] == 'id':
                continue
            if self.type == 'rooms':
                match table__name:
                    case 'lighting':
                        table__col = self.sqlite__cursor.execute(
                            f"SELECT {select__value_lighting} AS id__auto_switch FROM lighting WHERE id__room='{loc}'").fetchall()
                    case 'air__curtain':
                        table__col = self.sqlite__cursor.execute(
                            f"SELECT {select__value_air_curtain} AS id__auto_switch FROM air__curtain WHERE id__room='{loc}'").fetchall()
                    case 'conditioner':
                        table__col = self.sqlite__cursor.execute(
                            f"SELECT {select__value_conditioner} AS id__auto_switch FROM conditioner WHERE id__room='{loc}'").fetchall()
                    case 'electric__motor':
                        table__col = self.sqlite__cursor.execute(
                            f"SELECT {select__value_electric_motor} AS id__auto_switch FROM electric__motor WHERE id__room='{loc}'").fetchall()
                    case 'sockets':
                        table__col = self.sqlite__cursor.execute(
                            f"SELECT {select__value_sockets} AS id__auto_switch FROM sockets WHERE id__room='{loc}'").fetchall()
                    case 'switch':
                        table__col = self.sqlite__cursor.execute(
                            f"SELECT {select__value_switch} AS id__auto_switch FROM switch WHERE id__room='{loc}'").fetchall()
                    case 'shield':
                        table__col = self.sqlite__cursor.execute(
                            f"SELECT {select__value_shield} FROM shield WHERE id__room='{loc}'").fetchall()
                    case 'transformer':
                        table__col = self.sqlite__cursor.execute(
                            f"SELECT {select__value_transformer} FROM transformer WHERE id__room='{loc}'").fetchall()
            elif self.type == 'shield':
                match table__name:
                    case 'cable':
                        table__col = self.sqlite__cursor.execute(
                            f"SELECT cable.name, cable.manufacturer, cable.mark, cable.material, cable.number__of_cores, "
                            f"cable.cross__section, cable.length, cable.id__shield, auto__switch.name"
                            f" FROM cable JOIN auto__switch ON auto__switch.id=cable.id__auto_switch"
                            f" WHERE cable.id__shield='{loc}'").fetchall()
                    case 'auto__switch':
                        select__value_auto_switch = f"""SELECT a.name, a.manufacturer, a.type, a.size, a.characteristic,\
                        a.cutoff__current, a.leakage__current, a.id__shield, \
                        (CASE WHEN a2.name IS null THEN tr.id__transformer ELSE a2.id__shield || a2.name END) AS id__auto_switch \
                        FROM auto__switch AS a \
                        LEFT JOIN auto__switch AS a2 ON a.id__auto_switch=a2.id \
                        LEFT JOIN transformer AS tr ON a.id__auto_switch=tr.id__transformer \
                        WHERE a.id__shield='{loc}'"""
                        try:
                            table__col = self.sqlite__cursor.execute(select__value_auto_switch).fetchall()
                        except sqlite3.Error as err:
                            print(err)
        table = '<table><tbody><tr>'
        for name in name_col:
            table = table + f"<th>{name}</th>"
        table = table + "</tr>"
        for val in table__col:
            table = table + "<tr>"
            for value in val:
                table = table + f"<td>{value}</td>"
            table = table + "</tr>"
        table = table + "</tbody></table>"
        background__color_table = "<style>table {width: 100%;margin: 0px;border: 1px solid #dddddd;border-collapse: collapse;}\
        table th {font-weight: bold;padding: 5px;background: #efefef;border: 1px solid #dddddd;}\
        table td {border: 1px solid #dddddd;padding: 5px;}</style>"
        html = background__color_table + table
        wd = QDialog(self)
        wd.setWindowTitle(f'{equipment__type[self.sender().objectName()]} в {loc}')
        wd.setMinimumSize(1024, 400)
        whtml = QWebEngineView()
        whtml.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        whtml.setHtml(html)
        # whtml.setUrl(QUrl("https://www.google.com/"))
        wl = QVBoxLayout()
        wl.setContentsMargins(5, 5, 5, 0)
        wl.addWidget(whtml)
        frame__btn = QFrame()
        frame__btn.setContentsMargins(0, 0, 0, 5)
        frame__layout_btn = QHBoxLayout()
        # btn__print = QPushButton("Печать на прямую не работает")
        # btn__print.clicked.connect(lambda: self.print(whtml))
        btn__save = QPushButton("Сохранить в pdf")
        btn__save.setIcon(QIcon("../icon/checked.png"))
        btn__save.setStyleSheet("width: 200px")
        save__name_file = f'{equipment__type[self.sender().objectName()]} в {loc}'
        btn__save.clicked.connect(lambda: self.save(whtml, save__name_file))
        # frame__layout_btn.addWidget(btn__print)
        frame__layout_btn.addStretch(1)
        frame__layout_btn.addWidget(btn__save)
        frame__btn.setLayout(frame__layout_btn)
        wl.addWidget(frame__btn)
        wd.setLayout(wl)
        wd.show()
        if wd.exec() == 0:
            whtml.close()
            del whtml

    def print(self, whtml):
        return
        # whtml.page().printToPdf()
    def save(self, whtml, name):
        save__pdf, _ = QFileDialog.getSaveFileName(self, "Сохранить в PDF", f"./{name}", "PDF Files (*.pdf)")
        if save__pdf:
            whtml.page().printToPdf(save__pdf)

    def open__file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', './', "Data (*.db)")
        if not file:
            return
        config__write_path_data = configparser.ConfigParser()
        # path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
        config__write_path_data.read(f"{self.path}\settings.ini")
        config__write_path_data.set("path__database", "path", f"{file}")
        with open(f'{self.path}\settings.ini', 'w') as configfile:
            config__write_path_data.write(configfile)
        self.sqlite__connect.close()
        self.sqlite__connect = sqlite3.connect(file)
        self.sqlite__cursor = self.sqlite__connect.cursor()
        self.equipment__type_items()

    def load__settings(self, val):
        if val == "db":
            config = configparser.ConfigParser()  # создаём объекта парсера
            # path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
            config.read(f"{self.path}/settings.ini")
            # print(config)
            # config.read("./settings.ini")  # читаем конфиг
            # print(config)
            res = config["path__database"]["path"]
            return res  # обращаемся как к обычному словарю!
    def windowUI(self):
        # self.setStyleSheet("QMainWindow {color: qlineargradient(spread:pad, x1:0 y1:0, x2:1 y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));"
        #                "background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #12100E, stop:1 #2B4162);}")
        # add layout
        self.layout__combobox_top = QHBoxLayout()
        self.layout__central_info = QVBoxLayout()
        # setings layout

        # add element
        self.box__combobox_top = QFrame(self)
        self.box__combobox_top.setObjectName("box__combobox_top")
        self.box__group_central = QGroupBox(self)
        self.box__group_central.setObjectName("box__group_central")
        self.equipment__qcombobox = QComboBox()
        self.equipment__qcombobox.setObjectName("equipment__qcombobox")
        self.equipment__location_qcombobox = QComboBox()
        self.equipment__location_qcombobox.setObjectName("equipment__location_qcombobox")
        self.equipment__unit_qcombobox = QComboBox()
        self.equipment__unit_qcombobox.setObjectName("equipment__unit_qcombobox")
        self.btn__add = QPushButton()
        self.btn__change = QPushButton()
        self.btn__remove = QPushButton()
        self.btn__add.setText('&Добавить')
        self.btn__change.setText('&Изминить')
        self.btn__remove.setText('&Удалить')
        # setings element
        self.box__combobox_top.setGeometry(0, 43, 730, 50)
        self.box__combobox_top.setContentsMargins(0, 0, 0, 0)
        self.box__group_central.setGeometry(10, 88, 440, 372)
        self.equipment__qcombobox.setMinimumWidth(130)
        self.equipment__location_qcombobox.setMinimumWidth(100)
        self.equipment__unit_qcombobox.setMinimumWidth(100)
        self.equipment__unit_qcombobox.setStyleSheet("QComboBox { combobox-popup: 0;}")
        # self.box__group_central.setTitle("fsdf")
        # add element to layout
        self.layout__combobox_top.addWidget(self.equipment__qcombobox)
        self.layout__combobox_top.addWidget(self.equipment__location_qcombobox)
        self.layout__combobox_top.addWidget(self.equipment__unit_qcombobox)
        self.layout__combobox_top.addStretch()
        self.layout__combobox_top.addWidget(self.btn__add)
        self.layout__combobox_top.addWidget(self.btn__change)
        self.layout__combobox_top.addWidget(self.btn__remove)
        # widget
        self.box__combobox_top.setLayout(self.layout__combobox_top)
        self.box__group_central.setLayout(self.layout__central_info)
        # signal
        self.btn__add.clicked.connect(lambda: self.equipment__add())
        self.btn__change.clicked.connect(lambda: self.equipment__change())
        self.btn__remove.clicked.connect(self.equipment__remove)
        self.equipment__qcombobox.currentTextChanged.connect(self.equipment__click)
        self.equipment__location_qcombobox.currentTextChanged.connect(self.equipment__location_click)
        self.equipment__unit_qcombobox.currentTextChanged.connect(self.show__info)
        # -----------------widget__right----------------
        self.widget__right = QWidget(self)
        self.widget__right.setContentsMargins(0, 0, 0, 0)
        self.widget__right.setStyleSheet("border-radius: 3px;")
        self.widget__right.setObjectName("widget__right")
        # self.blur_effect = QtWidgets.QGraphicsBlurEffect()
        # self.widget__right.setGraphicsEffect(self.blur_effect)
        self.widget__right.setGeometry(self.width() - 273, self.height() - 382, 263, 352)
        # self.img__sheme = QPixmap("../icon/change.png")
        # self.img__label = QLabel()
        # self.img__label.setMaximumSize(200, 200)
        # self.img__label.setPixmap(self.img__sheme)
        self.widget__right_grid = QGridLayout(self.widget__right)
        self.widget__right_grid.setContentsMargins(0, 0, 0, 0)
        self.widget__right_grid.setSpacing(0)
        # self.widget__right_grid.addWidget(self.img__label, 1, 4)

        self.equipment__type_items()

    def equipment__type_items(self):
        global equipment__type
        self.equipment__qcombobox.blockSignals(True)
        self.equipment__qcombobox.clear()
        for key, value in equipment__type.items():
            self.equipment__qcombobox.addItem(f"{value}", key)
        # for t in equipment__type.values():
        #     self.equipment__qcombobox.addItem(f"{str(t)}")
        self.equipment__qcombobox.blockSignals(False)
        self.equipment__click()

    def location__add_items(self, k): # доработать
        try:
            if k == 'auto__switch':
                self.equipment__location_qcombobox.clear()
                loc = self.sqlite__cursor.execute(f"SELECT DISTINCT id__shield FROM {k} ORDER BY id__shield").fetchall()
                for i in range(len(loc)):
                    self.equipment__location_qcombobox.addItem(str(loc[i][0]))
            elif k == 'rooms':
                self.equipment__location_qcombobox.clear()
                loc = self.sqlite__cursor.execute(f"SELECT id__room FROM {k} ORDER BY id__room").fetchall()
                self.equipment__unit_qcombobox.setEnabled(False)
                for i in range(len(loc)):
                    self.equipment__location_qcombobox.addItem(str(loc[i][0]))
            elif k == 'shield':
                self.equipment__location_qcombobox.clear()
                loc = self.sqlite__cursor.execute(f"SELECT id__shield FROM {k} ORDER BY id__shield").fetchall()
                for i in range(len(loc)):
                    self.equipment__location_qcombobox.addItem(str(loc[i][0]))
                self.equipment__unit_qcombobox.setEnabled(False)
            elif k == 'cable':
                self.equipment__location_qcombobox.clear()
                cable = self.sqlite__cursor.execute(f"SELECT name FROM {k} ORDER BY name").fetchall()
                for i in range(len(cable)):
                    self.equipment__location_qcombobox.addItem(str(cable[i][0]))
                self.equipment__unit_qcombobox.setEnabled(False)
            else:
                self.equipment__location_qcombobox.clear()
                loc = self.sqlite__cursor.execute(f"SELECT DISTINCT id__room FROM {k} ORDER BY id__room").fetchall()
                for i in range(len(loc)):
                    self.equipment__location_qcombobox.addItem(str(loc[i][0]))
        except sqlite3.Error as err:
            print(err)
        if self.equipment__location_qcombobox.currentText() == '':
            if self.layout__central_info.parentWidget().findChildren(QLabel):
                upd = self.layout__central_info.parentWidget().findChildren(QLabel)
                for d in upd:
                    d.deleteLater()
            if self.layout__central_info.parentWidget().findChildren(QPushButton):
                del__btn = self.layout__central_info.parentWidget().findChildren(QPushButton)
                for d in del__btn:
                    d.deleteLater()
            if self.layout__central_info.parentWidget().findChildren(QHBoxLayout):
                del__hl = self.layout__central_info.parentWidget().findChildren(QHBoxLayout)
                for d in del__hl:
                    d.deleteLater()

    def equipment__click(self):
        global equipment__type
        self.type = ''
        items__click = self.equipment__qcombobox.currentText()
        self.equipment__location_qcombobox.clear()
        self.equipment__unit_qcombobox.clear()
        self.equipment__unit_qcombobox.setEnabled(True)
        self.box__group_central.setTitle(items__click)
        for k, val in equipment__type.items():
            if val == items__click:
                self.type = k
                self.location__add_items(k)

    def equipment__location_click(self):
        b = 'True'
        if self.type:
            try:
                if self.type == 'shield':
                    self.show__info(b)
                elif self.type == 'cable':
                    self.show__info(b)
                elif self.type == 'rooms':
                    self.show__info(b)
                elif self.type == 'air__curtain':
                    self.equipment__unit_qcombobox.clear()
                    unit = self.sqlite__cursor.execute(
                        f"SELECT * FROM {self.type} WHERE id__room='{self.sender().currentText()}' ORDER BY name").fetchall()
                    for i in range(len(unit)):
                        self.equipment__unit_qcombobox.addItem(str(unit[i][1]))
                elif self.type == 'conditioner':
                    self.equipment__unit_qcombobox.clear()
                    unit = self.sqlite__cursor.execute(
                        f"SELECT * FROM {self.type} WHERE id__room='{self.sender().currentText()}' ORDER BY name").fetchall()
                    for i in range(len(unit)):
                        self.equipment__unit_qcombobox.addItem(str(unit[i][1]))
                elif self.type == 'electric__motor':
                    self.equipment__unit_qcombobox.clear()
                    unit = self.sqlite__cursor.execute(
                        f"SELECT * FROM {self.type} WHERE id__room='{self.sender().currentText()}' ORDER BY name").fetchall()
                    for i in range(len(unit)):
                        self.equipment__unit_qcombobox.addItem(str(unit[i][1]))
                elif self.type == 'lighting':
                    self.equipment__unit_qcombobox.clear()
                    unit = self.sqlite__cursor.execute(
                        f"SELECT id, name FROM {self.type} WHERE id__room='{self.sender().currentText()}' ORDER BY name").fetchall()
                    # print(unit)
                    # unit__str = ''
                    for i in range(len(unit)):
                        # unit__str = f'{unit[i][1]}, {unit[i][0]}'
                        # print(unit__str)
                        self.equipment__unit_qcombobox.addItem(str(unit[i][1]), unit[i][0])
                elif self.type == 'sockets':
                    self.equipment__unit_qcombobox.clear()
                    unit = self.sqlite__cursor.execute(
                        f"SELECT * FROM {self.type} WHERE id__room='{self.sender().currentText()}' ORDER BY name").fetchall()
                    for i in range(len(unit)):
                        self.equipment__unit_qcombobox.addItem(str(unit[i][1]))
                elif self.type == 'switch':
                    self.equipment__unit_qcombobox.clear()
                    unit = self.sqlite__cursor.execute(
                        f"SELECT * FROM {self.type} WHERE id__room='{self.sender().currentText()}' ORDER BY name").fetchall()
                    for i in range(len(unit)):
                        self.equipment__unit_qcombobox.addItem(str(unit[i][1]))
                elif self.type == 'transformer':
                    self.equipment__unit_qcombobox.clear()
                    unit = self.sqlite__cursor.execute(
                        f"SELECT * FROM {self.type} WHERE id__room='{self.sender().currentText()}' ORDER BY id__transformer").fetchall()
                    for i in range(len(unit)):
                        self.equipment__unit_qcombobox.addItem(str(unit[i][0]))
                elif self.type == 'auto__switch':
                    self.equipment__unit_qcombobox.clear()
                    unit = self.sqlite__cursor.execute(
                        f"SELECT * FROM {self.type} WHERE id__shield='{self.sender().currentText()}' ORDER BY name").fetchall()
                    for i in range(len(unit)):
                        self.equipment__unit_qcombobox.addItem(str(unit[i][1]))
            except sqlite3.Error as err:
                print(err)

    def show__info(self, bl='False'):
        val1 = self.equipment__qcombobox.currentText()
        val2 = self.equipment__location_qcombobox.currentText()
        val3 = self.equipment__unit_qcombobox.currentText()
        in__the_room = {}
        in__the_shield = {}
        temp__shield_value = ''
        if self.layout__central_info.parentWidget().findChildren(QLabel):
            upd = self.layout__central_info.parentWidget().findChildren(QLabel)
            for d in upd:
                d.deleteLater()
        if self.layout__central_info.parentWidget().findChildren(QPushButton):
            del__btn = self.layout__central_info.parentWidget().findChildren(QPushButton)
            for d in del__btn:
                d.deleteLater()
        if self.layout__central_info.parentWidget().findChildren(QHBoxLayout):
            del__hl = self.layout__central_info.parentWidget().findChildren(QHBoxLayout)
            for d in del__hl:
                d.deleteLater()
        if val1 and val2 and val3:
            try:
                if self.type == "transformer":
                    info = self.sqlite__cursor.execute(
                        f"SELECT * FROM {self.type} WHERE id__transformer='{val3}'").fetchall()
                elif self.type == "auto__switch":
                    info = self.sqlite__cursor.execute(
                        f"SELECT * FROM auto__switch WHERE name='{val3}' AND id__shield='{val2}'").fetchall()
                elif self.type == "lighting":
                    lighting__id = self.equipment__unit_qcombobox.currentData()
                    info = self.sqlite__cursor.execute(
                        f"SELECT * FROM {self.type} WHERE id='{lighting__id}'  AND id__room='{val2}'").fetchall()
                else:
                    info = self.sqlite__cursor.execute(
                        f"SELECT * FROM {self.type} WHERE name='{val3}'  AND id__room='{val2}'").fetchall()
                characteristics = self.sqlite__cursor.execute(f"pragma table_info({self.type})").fetchall()
                # print(info)
                for i in range(len(characteristics)):
                    if characteristics[i][1] == 'id':
                        pass
                    elif characteristics[i][1] == 'id__shield':
                        pass
                        # temp__shield_value = info[0][i]
                        # h__layout = QHBoxLayout(self)
                        # label = QLabel('Расположен:')
                        # h__layout.addWidget(label)
                        # h__layout.addStretch()
                        # label = QLabel(f'{info[0][i]}')
                        # h__layout.addWidget(label)
                        # self.layout__central_info.addLayout(h__layout)
                    elif characteristics[i][1] == 'id__auto_switch':
                        h__layout = QHBoxLayout()
                        label = QLabel('Запитан от:')
                        h__layout.addWidget(label)
                        # h__layout.setSpacing(10)
                        h__layout.addStretch()
                        sql__select_name = f"SELECT name, id__shield FROM auto__switch WHERE id='{info[0][i]}'"
                        qf__name = self.sqlite__cursor.execute(sql__select_name).fetchall()
                        if qf__name:
                            label = QLabel(f'{qf__name[0][1]}, {qf__name[0][0]}')
                        elif not qf__name:
                            energized = self.sqlite__cursor.execute(f"SELECT id__transformer FROM transformer WHERE id__transformer='{info[0][i]}'").fetchone()
                            # print(energized)
                            if energized:
                                label = QLabel(f'{energized[0]}')
                            else:
                                label = QLabel('не определено')
                        h__layout.addWidget(label)
                        self.layout__central_info.addLayout(h__layout)
                    else:
                        h__layout = QHBoxLayout()
                        label = QLabel(f'{characteristics__to[characteristics[i][1]]} :')
                        label.setObjectName(characteristics[i][1])
                        h__layout.addWidget(label)
                        # h__layout.setSpacing(10)
                        h__layout.addStretch()
                        label = QLabel(f'{info[0][i]}')
                        h__layout.addWidget(label)
                        self.layout__central_info.addLayout(h__layout)

            except sqlite3.Error as err:
                print(err)
        if bl == 'True' and val1 and val2:
            try:
                if self.type == "rooms":
                    # find__in_table = ['air__curtain', 'conditioner', 'electric__motor', 'lighting', 'rooms', 'shield', 'sockets', 'switch', 'transformer']
                    find__in_table = ['air__curtain', 'conditioner', 'electric__motor', 'lighting', 'shield', 'sockets', 'switch', 'transformer']
                    for key in find__in_table:
                        res = self.sqlite__cursor.execute(
                            f"SELECT * FROM {key} WHERE id__room='{val2}'").fetchall()
                        if res:
                            in__the_room.setdefault(key, res)
                    info = self.sqlite__cursor.execute(
                        f"SELECT * FROM {self.type} WHERE id__room='{val2}'").fetchall()
                elif self.type == 'cable':
                    info = self.sqlite__cursor.execute(
                        f"SELECT * FROM {self.type} WHERE name='{val2}'").fetchall()
                elif self.type == 'shield':
                    find__in_table = ['auto__switch', 'cable']
                    for key in find__in_table:
                        res = self.sqlite__cursor.execute(f"SELECT * FROM {key} WHERE id__shield='{val2}'").fetchall()
                        if res:
                            in__the_shield.setdefault(key, res)
                    info = self.sqlite__cursor.execute(
                        f"SELECT * FROM {self.type} WHERE id__shield='{val2}'").fetchall()
                characteristics = self.sqlite__cursor.execute(f"pragma table_info({self.type})").fetchall()

                for i in range(len(characteristics)):
                    if characteristics[i][1] == 'id':
                        pass
                    elif characteristics[i][1] == 'id__shield':
                        # temp__shield_value = info[0][i]
                        pass
                    elif characteristics[i][1] == 'id__auto_switch':
                        h__layout = QHBoxLayout()
                        label = QLabel('Запитан от:')
                        h__layout.addWidget(label)
                        # h__layout.setSpacing(10)
                        h__layout.addStretch()
                        sql__select_name = f"SELECT name, id__shield FROM auto__switch WHERE id='{info[0][i]}'"
                        qf__name = self.sqlite__cursor.execute(sql__select_name).fetchall()
                        if qf__name:
                            # label = QLabel(f'{temp__shield_value}, {qf__name[0][0]}')
                            label = QLabel(f'{qf__name[0][1]}, {qf__name[0][0]}')
                        else:
                            label = QLabel('не определено')
                        h__layout.addWidget(label)
                        self.layout__central_info.addLayout(h__layout)
                    else:
                        h__layout = QHBoxLayout()
                        label = QLabel(f'{characteristics__to[characteristics[i][1]]}')
                        label.setObjectName(characteristics[i][1])
                        h__layout.addWidget(label)
                        # h__layout.setSpacing(10)
                        h__layout.addStretch()
                        label = QLabel(f'{info[0][i]}')
                        h__layout.addWidget(label)
                        self.layout__central_info.addLayout(h__layout)

            except sqlite3.Error as err:
                print(err)
            if self.type == 'rooms':
                nurber__create_layout_room = 0
                lehgh = len(in__the_room)
                for key in in__the_room:
                    if nurber__create_layout_room == 0:
                        # lhb = QHBoxLayout()
                        self.ehb = QHBoxLayout()
                    if nurber__create_layout_room <= 2:
                        # label = QLabel(f"{key} = {len(in__the_room[key])}")
                        # label.setObjectName(f'key')
                        # label.mousePressEvent = self.mouse__press_label
                        # lhb.addWidget(self.equip__button)
                        name = equipment__type[key]
                        if len(name) > 7:
                            name = name[:7] + "..."
                        self.additionally__equip_button = QPushButton(f"{name} {len(in__the_room[key])} шт.")
                        # self.additionally__equip_button.setStyleSheet("font-size: 11px")
                        self.additionally__equip_button.setObjectName(f'{key}')
                        self.additionally__equip_button.clicked.connect(self.additionally__equip_info)
                        self.ehb.addWidget(self.additionally__equip_button)
                    lehgh -= 1
                    if nurber__create_layout_room == 2 or lehgh == 0:
                        nurber__create_layout_room = 0
                        self.layout__central_info.addLayout(self.ehb)
                        continue
                    nurber__create_layout_room = nurber__create_layout_room + 1
            if self.type == 'shield':
                number__create_layout_shield = 0
                lengh = len(in__the_shield)
                for key in in__the_shield:
                    if number__create_layout_shield == 0:
                        self.layout__btn = QHBoxLayout()
                    if number__create_layout_shield <= 2:
                        name = equipment__type[key]
                        if len(name) > 7:
                            name = name[:7] + "..."
                        self.additionally__equip_button = QPushButton(f"{name} {len(in__the_shield[key])} шт.")
                        # self.additionally__equip_button.setStyleSheet("font-size: 11px")
                        self.additionally__equip_button.setObjectName(f'{key}')
                        self.additionally__equip_button.clicked.connect(self.additionally__equip_info)
                        self.layout__btn.addWidget(self.additionally__equip_button)
                    lengh -= 1
                    if number__create_layout_shield == 2 or lengh == 0:
                        number__create_layout_shield = 0
                        self.layout__central_info.addLayout(self.layout__btn)
                        continue
                    number__create_layout_shield = number__create_layout_shield + 1
    def equipment__add(self):
        self.equip__add = EquipmentAdd(self, self.sqlite__connect, self.sqlite__cursor, equipment__type,
                                          characteristics__to)
        self.equip__add.exec()
        self.equipment__click()

    def equipment__change(self):
        if self.equipment__location_qcombobox.currentText() == '':
            return
        value = []
        val__temp = ''
        for k, val in equipment__type.items():
            if val == self.equipment__qcombobox.currentText():
                val__temp = k
        value.append(val__temp)
        value.append(self.equipment__location_qcombobox.currentText())
        if val__temp == 'lighting':
            if self.equipment__unit_qcombobox.currentText() != '':
                lighting__id = self.equipment__unit_qcombobox.currentData()
                value.append(lighting__id)
        elif self.equipment__unit_qcombobox.currentText() != '':
            value.append(self.equipment__unit_qcombobox.currentText())
        self.equip__change = EquipmentChange(self, self.sqlite__connect, self.sqlite__cursor, equipment__type,
                                          characteristics__to, value)
        self.equip__change.exec()
        self.equipment__click()


    def equipment__remove(self):
        global equipment__type
        text = 'Ваши действия приведут к необратимым изменением. Вы уверены?'
        rm = QMessageBox()
        rm.setWindowTitle("Удаление")
        rm.setText(text)
        rm.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        x = rm.exec()
        if x == QMessageBox.StandardButton.Yes:
            table = equipment__type.copy()
            match self.type:
                case 'rooms':
                    table2 = equipment__type.copy()
                    table3 = equipment__type.copy()
                    room = self.equipment__location_qcombobox.currentText()
                    keys = ['rooms', 'cable', 'auto__switch']
                    for key in keys:
                        table.pop(key, None)
                    keys2 = ['rooms', 'shield', 'transformer']
                    for key in keys2:
                        table2.pop(key, None)
                    try:
                        sql__delete_room = f"DELETE FROM rooms WHERE id__room='{room}'"
                        for t in table:
                            if t == 'shield':
                                id__shield = self.sqlite__cursor.execute(
                                    f"SELECT id__shield FROM shield WHERE id__room='{room}'").fetchall()
                                if id__shield:
                                    for shield in id__shield:
                                        id__auto_switch = self.sqlite__cursor.execute(f"SELECT id FROM auto__switch WHERE id__shield='{shield[0]}'").fetchall()
                                        if id__auto_switch:
                                            for id in id__auto_switch:
                                                self.sqlite__cursor.execute(f"DELETE FROM auto__switch WHERE id='{id[0]}'")
                                                for i in table2:
                                                    self.sqlite__cursor.execute(
                                                        f"UPDATE {i} SET id__auto_switch='removed', id__shield='Удаленные' "
                                                        f"WHERE id__auto_switch='{id[0]}'")
                                        self.sqlite__cursor.execute(f"DELETE FROM shield WHERE id__shield='{shield[0]}'")
                                self.sqlite__connect.commit()
                            elif t == 'transformer':
                                try:
                                    sql__delete = f"DELETE FROM transformer WHERE id__room='{room}'"
                                    self.sqlite__cursor.execute(sql__delete)
                                    id__transformer = self.sqlite__cursor.execute(f"SELECT id__transformer FROM transformer WHERE id__room='{room}'").fetchall()
                                    if id__transformer:
                                        keys3 = ['rooms', 'shield']
                                        for key in keys3:
                                            table3.pop(key, None)
                                        for val in id__transformer:
                                            for t in table3:
                                                self.sqlite__cursor.execute(f"UPDATE {t} SET id__auto_switch='Удален' WHERE id__auto_switch='{val[0]}'")
                                    self.sqlite__connect.commit()
                                except sqlite3.Error as err:
                                    print(err)
                            else:
                                self.sqlite__cursor.execute(f"DELETE FROM {t} WHERE id__room='{room}'")
                        self.sqlite__cursor.execute(sql__delete_room)
                        self.sqlite__connect.commit()
                    except sqlite3.Error as err:
                        print(err)
                    self.equipment__click()
                case 'shield':
                    shield = self.equipment__location_qcombobox.currentText()
                    sql__select_auto_switch = f"SELECT id FROM auto__switch WHERE id__shield='{shield}'"
                    sql__delete_shield = f"DELETE FROM shield WHERE id__shield='{shield}'"
                    keys = ['rooms', 'shield', 'transformer']
                    for key in keys:
                        table.pop(key, None)
                    try:
                        id__auto_switch = self.sqlite__cursor.execute(sql__select_auto_switch).fetchall()
                        for v in id__auto_switch:
                            # print(v)
                            self.sqlite__cursor.execute(f"DELETE from auto__switch WHERE id='{v[0]}'")
                            for t in table:
                                self.sqlite__cursor.execute(f"UPDATE {t} SET id__auto_switch='removed', id__shield='Удаленные' "
                                                            f"WHERE id__auto_switch='{v[0]}'")
                        self.sqlite__cursor.execute(sql__delete_shield)
                        self.sqlite__connect.commit()
                    except sqlite3.Error as err:
                        print(err)
                    self.equipment__click()
                case 'transformer':
                    room = self.equipment__location_qcombobox.currentText()
                    name = self.equipment__unit_qcombobox.currentText()
                    try:
                        sql__delete = f"DELETE FROM transformer WHERE id__room='{room}' " \
                                      f"AND id__transformer='{name}'"
                        self.sqlite__cursor.execute(sql__delete)
                        keys = ['rooms', 'shield']
                        for key in keys:
                            table.pop(key, None)
                        for t in table:
                            sql__update = f"UPDATE {t} SET id__auto_switch='removed' " \
                                          f"WHERE id__auto_switch='{name}'"
                            self.sqlite__cursor.execute(sql__update)
                        self.sqlite__connect.commit()
                    except sqlite3.Error as err:
                        print(err)
                    self.equipment__click()
                case 'cable':
                    name = self.equipment__location_qcombobox.currentText()
                    try:
                        sql__delete = f"DELETE FROM cable WHERE name='{name}'"
                        self.sqlite__cursor.execute(sql__delete)
                        self.sqlite__connect.commit()
                    except sqlite3.Error as err:
                        print(err)
                    self.equipment__click()
                case 'auto__switch':
                    shield = self.equipment__location_qcombobox.currentText()
                    name = self.equipment__unit_qcombobox.currentText()
                    id = self.sqlite__cursor.execute(f"SELECT id FROM auto__switch "
                                                     f"WHERE id__shield='{shield}' AND name='{name}'").fetchone()[0]
                    try:
                        sql__delete = f"DELETE FROM auto__switch WHERE id='{id}'"
                        self.sqlite__cursor.execute(sql__delete)
                        keys = ['rooms', 'shield', 'transformer']
                        for key in keys:
                            table.pop(key, None)
                        for t in table:
                            sql__update = f"UPDATE {t} SET id__auto_switch='removed' " \
                                          f"WHERE id__auto_switch='{id}'"
                            self.sqlite__cursor.execute(sql__update)
                        self.sqlite__connect.commit()
                    except sqlite3.Error as err:
                        print(err)
                    self.equipment__click()
                case 'lighting':
                    try:
                        lighting__delete_sql = f"DELETE FROM lighting WHERE id='{self.equipment__unit_qcombobox.currentData()}'"
                        self.sqlite__cursor.execute(lighting__delete_sql)
                        self.sqlite__connect.commit()
                    except sqlite3.Error as err:
                        print(err)
                    self.equipment__click()
                case _:
                    try:
                        sql__delete = f"DELETE FROM {self.type} WHERE id__room='{self.equipment__location_qcombobox.currentText()}' " \
                                      f"AND name='{self.equipment__unit_qcombobox.currentText()}'"
                        self.sqlite__cursor.execute(sql__delete)
                        self.sqlite__connect.commit()
                    except sqlite3.Error as err:
                        print(err)
                    self.equipment__click()
# print(self.equipment__qcombobox.itemData(self.equipment__qcombobox.currentIndex()))
#             id__room, id__shield, id__transformer
# two parametrs cable, rooms, shield

if __name__ == "__main__":
    app = QApplication(sys.argv)
    id = QFontDatabase.addApplicationFont(f"{path}/font/OpenSans.ttf")
    if id < 0:
        print("Error")
    else:
        families = QFontDatabase.applicationFontFamilies(id)
        app.setFont(QFont(families[0], 50))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())