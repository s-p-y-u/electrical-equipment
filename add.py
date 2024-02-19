import sqlite3
from PyQt6.QtWidgets import (QComboBox, QDialog, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QSpinBox, QVBoxLayout, QFrame)

class EquipmentAdd(QDialog):
    def __init__(self, parent=None, sqlite__connect=None, sqlite__cursor=None, equipment__type=None, characteristics__to=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить оборудование")
        self.window().adjustSize()
        self.setMinimumWidth(240)
        self.setMaximumWidth(300)
        self.sqlite__connect = sqlite__connect
        self.sqlite__cursor = sqlite__cursor
        self.equipment__type = equipment__type
        self.characteristics__to = characteristics__to
        self.UI()

    def UI(self):
        self.type__combobox = QComboBox()
        self.main__layout = QVBoxLayout(self)
        self.main__layout.addWidget(self.type__combobox)
        # self.save = QPushButton('Сохранить')
        # self.save.clicked.connect(self.saved)
        # self.close = QPushButton('Закрыть')
        # self.close.clicked.connect(self.closed)
        # self.main__layout.addStretch(1)
        self.main__layout.setSpacing(5)
        # self.main__layout.setContentsMargins(0,0,0,0)
        self.equip = self.sqlite__cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        # self.start = self.sqlite__cursor.execute("SELECT EXISTS (SELECT * FROM transformer)").fetchone()
        self.type__combobox.currentIndexChanged.connect(self.characteristics__show)
        # self.type__combobox.blockSignals(True)
        for i in range(len(self.equip)):
            if self.equip[i][0] != 'sqlite_sequence':
                self.type__combobox.addItem(self.equipment__type[self.equip[i][0]])
        # self.type__combobox.blockSignals(False)

    def characteristics__show(self):
        self.del__label = self.main__layout.parentWidget().findChildren(QLabel)
        self.del__edit = self.main__layout.parentWidget().findChildren(QLineEdit)
        self.del__combobox = self.main__layout.parentWidget().findChildren(QComboBox)
        self.del__spinbox = self.main__layout.parentWidget().findChildren(QSpinBox)
        self.del__btn = self.main__layout.parentWidget().findChildren(QPushButton)
        self.blockSignals(True)
        if self.del__label:
            for dl in self.del__label:
                dl.deleteLater()
        if self.del__edit:
            for de in self.del__edit:
                de.clear()
                de.deleteLater()
        if self.del__spinbox:
            for ds in self.del__spinbox:
                ds.clear()
                ds.deleteLater()
        if self.del__combobox:
            for dc in self.del__combobox:
                if dc != self.type__combobox:
                    # dc.clear()
                    dc.deleteLater()
        if self.del__btn:
            for b in self.del__btn:
                b.deleteLater()
        self.blockSignals(False)
        # self.window().adjustSize()
        # self.main__layout.minimumSize()
        if self.sqlite__cursor:
            try:
                for k, v in self.equipment__type.items():
                    if v == self.sender().currentText():
                        self.type = k
                self.characteristics = self.sqlite__cursor.execute(f"pragma table_info({self.type})").fetchall()
                for i in range(len(self.characteristics)):
                    if self.characteristics[i][1] != 'id':
                        if self.characteristics[i][1] == 'size' and self.type == 'auto__switch':
                            self.label = QLabel('Размер')
                        elif self.characteristics[i][1] == 'id__auto_switch' and self.type == 'auto__switch':
                            self.label = QLabel('Запитан от')
                        elif self.characteristics[i][1] == 'lamp__quantity' and self.type == 'lighting':
                            self.label = ''
                        elif self.characteristics[i][1] == 'nominal__voltage' and self.type == 'electric__motor':
                            self.label = QLabel('Напрежение, ток, скорость')
                        elif self.characteristics[i][1] == 'nominal__current' and self.type == 'electric__motor':
                            self.label = ''
                        elif self.characteristics[i][1] == 'nominal__speed' and self.type == 'electric__motor':
                            self.label = ''
                        elif self.characteristics[i][1] == 'weight' and self.type == 'electric__motor':
                            self.label = QLabel('Вес, габариты')
                        elif self.characteristics[i][1] == 'size' and self.type == 'electric__motor':
                            self.label = ''
                        else:
                            self.label = QLabel(f'{self.characteristics__to[self.characteristics[i][1]]}')
                        if self.label != '':
                            self.label.setObjectName(self.characteristics[i][1])
                            self.main__layout.addWidget(self.label)
                        if self.characteristics[i][1] == 'id__shield' and self.type != 'shield':
                            self.combobox = QComboBox()
                            self.combobox.setObjectName(f'{self.characteristics[i][1]}')
                            shield__select = "SELECT id__shield FROM shield"
                            shield__result = self.sqlite__cursor.execute(shield__select).fetchall()
                            self.combobox.blockSignals(True)
                            for item in range(len(shield__result)):
                                self.combobox.addItem(shield__result[item][0])
                            # self.combobox.currentIndexChanged.connect(self.insert__switch)
                            self.combobox.currentTextChanged.connect(lambda:
                                                        self.insert__switch() if self.type != 'auto__switch' else False)
                            self.main__layout.addWidget(self.combobox)
                            self.combobox.blockSignals(False)
                            # self.combobox.setCurrentIndex(1)
                        elif self.characteristics[i][1] == 'id__auto_switch':
                            if self.type == "auto__switch":
                                self.combobox = QComboBox()
                                self.combobox.setObjectName(f'{self.characteristics[i][1]}')
                                self.combobox.setEditable(True)
                                self.combobox.currentTextChanged.connect(self.in__auto_swich)
                                self.main__layout.addWidget(self.combobox)
                            else:
                                self.combobox = QComboBox()
                                self.combobox.setObjectName(f'{self.characteristics[i][1]}')
                                self.main__layout.addWidget(self.combobox)
                                try:
                                    sql__switch = f"SELECT name FROM auto__switch WHERE id__shield='{self.findChild(QComboBox, 'id__shield').currentText()}'"
                                    res__switch = self.sqlite__cursor.execute(sql__switch).fetchall()
                                    if res__switch:
                                        for i in range(len(res__switch)):
                                            self.combobox.addItem(res__switch[i][0])
                                except sqlite3.Error as err:
                                    print(err)
                                # self.add__cable()
                        elif self.characteristics[i][1] == 'id__room' and self.type != 'rooms':
                            self.combobox = QComboBox()
                            self.combobox.setObjectName(f'{self.characteristics[i][1]}')
                            room__select = "SELECT id__room FROM rooms"
                            room__result = self.sqlite__cursor.execute(room__select).fetchall()
                            for item in range(len(room__result)):
                                self.combobox.addItem(str(room__result[item][0]))
                            self.main__layout.addWidget(self.combobox)
                        elif self.characteristics[i][1] == 'type':
                            self.combobox = QComboBox()
                            self.combobox.setObjectName(f'{self.characteristics[i][1]}')
                            self.combobox.addItem('Диф')
                            self.combobox.addItem('Узо')
                            self.combobox.addItem('Автомат')
                            self.combobox.addItem('Рубильник')
                            self.combobox.currentTextChanged.connect(lambda t=self.sender().objectName(): self.type__switch(t))
                            self.main__layout.addWidget(self.combobox)
                        elif self.type == 'lighting' and self.characteristics[i][1] == 'name':
                            self.line__edit = QLineEdit()
                            self.spin__quantity = QSpinBox()
                            self.spin__quantity.setMinimum(1)
                            self.spin__quantity.setMaximum(999)
                            self.frame__name_and_quantity = QFrame()
                            # self.frame__name_and_quantity.setContentsMargins(0,0,0,0)
                            self.layout__name_and_quantity = QHBoxLayout()
                            self.layout__name_and_quantity.setContentsMargins(0, 0, 0, 0)
                            self.line__edit.setObjectName(f'{self.characteristics[i][1]}')
                            self.spin__quantity.setObjectName('lighting__quantity')
                            # self.spin__quantity.lineEdit().setEnabled(False)
                            # self.spin__quantity.lineEdit().setReadOnly(True)
                            self.layout__name_and_quantity.addWidget(self.line__edit)
                            self.layout__name_and_quantity.addWidget(self.spin__quantity)
                            self.frame__name_and_quantity.setLayout(self.layout__name_and_quantity)
                            self.main__layout.addWidget(self.frame__name_and_quantity)
                        elif self.type == 'lighting' and self.characteristics[i][1] == 'lamp__type':
                            self.line__edit = QLineEdit()
                            self.spin__lamp__quantity = QSpinBox()
                            self.spin__lamp__quantity.setMinimum(1)
                            self.spin__lamp__quantity.setMaximum(999)
                            self.frame__lamp__quantity = QFrame()
                            self.layout__lamp__quantity = QHBoxLayout()
                            self.layout__lamp__quantity.setContentsMargins(0, 0, 0, 0)
                            self.line__edit.setObjectName(f'{self.characteristics[i][1]}')
                            self.spin__lamp__quantity.setObjectName('lamp__quantity')
                            # self.spin__lamp__quantity.lineEdit().setEnabled(False)
                            # self.spin__lamp__quantity.lineEdit().setReadOnly(True)
                            self.layout__lamp__quantity.addWidget(self.line__edit)
                            self.layout__lamp__quantity.addWidget(self.spin__lamp__quantity)
                            self.frame__lamp__quantity.setLayout(self.layout__lamp__quantity)
                            self.main__layout.addWidget(self.frame__lamp__quantity)
                        elif self.type == 'lighting' and self.characteristics[i][1] == 'lamp__quantity':
                            pass
                        # elif self.characteristics[i][1] == 'id__cable':
                        #     self.name__cable = QComboBox()
                        #     self.name__cable.setObjectName(f'{self.characteristics[i][1]}')
                        #     self.add__cable()
                        #     self.main__layout.addWidget(self.name__cable)
                        elif self.type == 'electric__motor' and self.characteristics[i][1] == 'nominal__voltage':
                            self.electric__motor_frame = QFrame()
                            self.electric__motor_frame_hlayout = QHBoxLayout()
                            self.electric__motor_frame_hlayout.setContentsMargins(0, 0, 0, 0)
                            self.electro__motor_comboBox = QComboBox()
                            self.electro__motor_comboBox.setObjectName(f'{self.characteristics[i][1]}')
                            self.electro__motor_comboBox.setMinimumWidth(70)
                            self.electro__motor_comboBox.addItem('220')
                            self.electro__motor_comboBox.addItem('380')
                            self.electric__motor_frame_hlayout.addWidget(self.electro__motor_comboBox)
                            self.line__edit_current = QLineEdit()
                            self.line__edit_current.setObjectName('nominal__current')
                            self.line__edit_current.setMinimumWidth(70)
                            self.electric__motor_frame_hlayout.addWidget(self.line__edit_current)
                            self.line__edit_speed = QLineEdit()
                            self.line__edit_speed.setObjectName('nominal__speed')
                            self.line__edit_speed.setMinimumWidth(70)
                            self.electric__motor_frame_hlayout.addWidget(self.line__edit_speed)
                            self.electric__motor_frame.setLayout(self.electric__motor_frame_hlayout)
                            self.main__layout.addWidget(self.electric__motor_frame)
                        elif self.type == 'electric__motor' and self.characteristics[i][1] == 'nominal__current':
                            pass
                        elif self.type == 'electric__motor' and self.characteristics[i][1] == 'nominal__speed':
                            pass
                        elif self.type == 'electric__motor' and self.characteristics[i][1] == 'weight':
                            self.electric__motor_frame = QFrame()
                            self.electric__motor_frame_hlayout = QHBoxLayout()
                            self.electric__motor_frame_hlayout.setContentsMargins(0, 0, 0, 0)
                            self.line__edit_weight = QLineEdit()
                            self.line__edit_weight.setObjectName('weight')
                            self.line__edit_weight.setMinimumWidth(70)
                            self.electric__motor_frame_hlayout.addWidget(self.line__edit_weight)
                            self.line__edit_size = QLineEdit()
                            self.line__edit_size.setObjectName('size')
                            self.line__edit_size.setMinimumWidth(70)
                            self.electric__motor_frame_hlayout.addWidget(self.line__edit_size)
                            self.electric__motor_frame.setLayout(self.electric__motor_frame_hlayout)
                            self.main__layout.addWidget(self.electric__motor_frame)
                        elif self.type == 'electric__motor' and self.characteristics[i][1] == 'size':
                            pass
                        elif self.type == 'electric__motor' and self.characteristics[i][1] == 'motor__starting_method':
                            self.combobox = QComboBox()
                            self.combobox.setObjectName(f'{self.characteristics[i][1]}')
                            self.combobox.addItem('Треугольник')
                            self.combobox.addItem('Звезда')
                            self.main__layout.addWidget(self.combobox)
                        else:
                            self.line__edit = QLineEdit()
                            self.line__edit.setObjectName(f'{self.characteristics[i][1]}')
                            self.main__layout.addWidget(self.line__edit)
                # self.save.clicked.connect(self.saved)
                # self.close.clicked.connect(self.closed)
                self.save = QPushButton('&Сохранить')
                self.save.setStyleSheet("margin-top: 10px")
                self.save.clicked.connect(self.saved)
                self.close = QPushButton('&Закрыть')
                self.close.clicked.connect(self.closed)
                self.main__layout.addWidget(self.save)
                self.main__layout.addWidget(self.close)
            except sqlite3.Error as err:
                print(err)
        self.window().adjustSize()


    # def add__cable(self):
    #     cable = self.findChild(QComboBox, 'id__cable')
    #     print(cable)
    #     try:
    #         shield = self.findChild(QComboBox, 'id__shield').currentText()
    #         auto__switch = self.findChild(QComboBox, 'id__auto_switch').currentText()
    #         sql = f"SELECT name FROM cable WHERE id__shield='{shield}' AND id__auto_switch='{auto__switch}'"
    #         res = self.sqlite__cursor.execute(sql).fetchall()
    #         print(res)
    #         if res:
    #             for i in range(len(res)):
    #                 cable.addItem(res[i][0])
    #     except sqlite3.Error as err:
    #         print(err)

    def insert__switch(self):
        text__shield = self.main__layout.parentWidget().findChild(QComboBox, "id__shield").currentText()
        add__switch = self.main__layout.parentWidget().findChild(QComboBox, "id__auto_switch")
        add__switch.blockSignals(True)
        add__switch.clear()
        add__switch.blockSignals(False)
        try:
            sql__switch = f"SELECT name FROM auto__switch WHERE id__shield='{text__shield}'"
            res__switch = self.sqlite__cursor.execute(sql__switch).fetchall()
            if res__switch:
                for i in range(len(res__switch)):
                    add__switch.addItem(res__switch[i][0])
        except sqlite3.Error as err:
            print(err)

    def in__auto_swich(self):
        self.sender().setEnabled(True)
        self.sender().setStyleSheet("color: rgb(216, 211, 205);")
        text = self.sender().currentText()
        self.sender().blockSignals(True)
        self.sender().clear()
        self.sender().addItem(text)
        self.sender().blockSignals(False)
        if len(text) > 1:
            # self.sender().setStyleSheet("QComboBox:editable {color: black;}")
            t = text.split(',')
            if len(t) > 1:
                t1 = t[0].strip()
                t2 = t[1].strip()
                sql = f"SELECT id, id__shield, name FROM auto__switch WHERE id__shield='{t1}' AND name LIKE '{t2}%' ORDER BY id__shield, name"
            elif t[0] == '':
                sql = ''
            else:
                t1 = t[0].strip()
                sql = f"SELECT id, id__shield, name FROM auto__switch WHERE id__shield LIKE '{t1}%' ORDER BY id__shield, name"
            try:
                if sql != '':
                    res = self.sqlite__cursor.execute(sql).fetchall()
                else:
                    res = ''

                if res:
                    for ii in range(len(res)):
                        # found__values_switch.append(res[ii][1])
                        self.sender().addItem(f"{res[ii][1]}, {res[ii][2]}")
                else:
                    sql__select_transformer = f"SELECT id__transformer FROM transformer"
                    res__transformer = self.sqlite__cursor.execute(sql__select_transformer).fetchall()
                    if res__transformer:
                        for iii in range(len(res__transformer)):
                            self.sender().addItem(res__transformer[iii][0])
                    else:
                        pass
                        # self.sender().addItem("Нет соответствующих записей")
                        # self.sender().setEnabled(False)
                # self.sender()
            except sqlite3.Error as err:
                print(err)
            # self.sender().showPopup()
        else:
            pass

    def type__switch(self, t):
        type = self.main__layout.parentWidget().findChild(QLineEdit, 'leakage__current')
        type2 = self.main__layout.parentWidget().findChild(QLineEdit, 'cutoff__current')
        type3 = self.main__layout.parentWidget().findChild(QLineEdit, 'characteristic')
        if t == 'Узо':
            type.setEnabled(True)
            type2.setEnabled(True)
            type3.setEnabled(False)
            type3.setText("none")
            type2.setText('')
            type.clear()
        elif t == 'Диф':
            type.setEnabled(True)
            type2.setEnabled(True)
            type3.setEnabled(True)
            type.clear()
            type2.clear()
            type3.clear()
        elif t == 'Автомат':
            type.setEnabled(False)
            type.setText('none')
            type2.setEnabled(True)
            type2.clear()
            type3.setEnabled(True)
            type3.setText('')
        else:
            type.setEnabled(False)
            type.setText("none")
            type2.setEnabled(True)
            type2.setText('')
            type3.setEnabled(False)
            type3.setText('none')

    def saved(self):
        param1 = self.main__layout.parentWidget().findChildren(QLineEdit)
        param2 = self.main__layout.parentWidget().findChildren(QComboBox)
        q = ''
        if self.type == 'lighting':
            spin = self.main__layout.parentWidget().findChildren(QSpinBox)
            param1.remove(spin[0].lineEdit())
            param1.remove(spin[1].lineEdit())
            q = spin[0].value()
        param2.remove(self.type__combobox)
        self.save__param = {}
        self.not__null = 'True'
        shield = ''
        name = ''
        room = ''
        usl = ''

        for val in param1:
            if val.text() == '':
                self.not__null = 'False'
                val.setFocus()
                return
            if val.objectName() == 'name':
                name = val.text().strip()
                focus__name = val
            if val.objectName() == 'id__shield' and self.type == 'shield':
                shield = val.text().strip()
                focus__shield = val
            if val.objectName() == 'id__room' and self.type == 'rooms':
                room = val.text().strip()
                focus__room = val
            if val.objectName() == 'id__transformer' and self.type == 'transformer':
                transformer = val.text().strip()
                focus__transformer = val
        for val in param2:
            if val.currentText() == '':
                self.not__null = 'False'
                val.setFocus()
                return
            if val.objectName() == 'id__shield' and self.type != 'shield':
                shield = val.currentText()
            if val.objectName() == 'id__room' and self.type != 'rooms':
                room = val.currentText()
            if val.objectName() == 'id__transformer' and self.type != 'transformer':
                transformer = val.currentText()
        if self.not__null == 'True':
            match self.type:
                case 'auto__switch':
                    usl = int(self.sqlite__cursor.execute(
                        f"SELECT EXISTS(SELECT * FROM auto__switch WHERE id__shield='{shield}' "
                        f"AND name='{name}')").fetchone()[0])
                    if usl == 1:
                        focus__name.setFocus()
                        return
                case 'cable':
                    usl = int(self.sqlite__cursor.execute(
                        f"SELECT EXISTS(SELECT name FROM cable WHERE name='{name}')").fetchone()[0])
                    if usl == 1:
                        focus__name.setFocus()
                        return
                case 'rooms':
                    usl = int(self.sqlite__cursor.execute(
                            f"SELECT EXISTS(SELECT id__room FROM rooms WHERE id__room='{room}')").fetchone()[0])
                    if usl == 1:
                        focus__room.setFocus()
                        return
                case 'shield':
                    usl = int(self.sqlite__cursor.execute(
                        f"SELECT EXISTS(SELECT id__shield FROM shield WHERE id__shield='{shield}')").fetchone()[0])
                    if usl == 1:
                        focus__shield.setFocus()
                        return
                case 'transformer':
                    usl = int(self.sqlite__cursor.execute(
                        f"SELECT EXISTS(SELECT id__transformer FROM transformer "
                        f"WHERE id__transformer='{transformer}')").fetchone()[0])
                    if usl == 1:
                        focus__transformer.setFocus()
                        return
                case 'lighting':
                    usl = 0
                case _:
                    usl = int(self.sqlite__cursor.execute(
                        f"SELECT EXISTS(SELECT * FROM {self.type} WHERE name='{name}' "
                        f"AND id__room='{room}')").fetchone()[0])
                    if usl == 1:
                        focus__name.setFocus()
                        return
            if usl == 0:
                for val in param2:
                    if val.objectName() == "id__auto_switch" and self.type == "auto__switch":
                        try:
                            t = val.currentText().find(',')
                            if t != -1:
                                s, n = val.currentText().split(",")
                                n = n.lstrip()
                                sql__id = f"SELECT id FROM auto__switch WHERE id__shield='{s}' AND name='{n}'"
                                res__sql_id = self.sqlite__cursor.execute(sql__id).fetchall()
                                self.save__param.setdefault(f'{val.objectName()}', res__sql_id[0][0])
                            else:
                                tr = val.currentText().strip()
                                u = int(self.sqlite__cursor.execute(f"SELECT EXISTS(SELECT id__transformer FROM transformer WHERE id__transformer='{tr}')").fetchone()[0])
                                if u == 0:
                                    val.setFocus()
                                    val.setStyleSheet("color: red")
                                    return
                                self.save__param.setdefault(f'{val.objectName()}', tr)
                        except sqlite3.Error as err:
                            print(err)
                    elif val.objectName() == "id__auto_switch" and self.type != "auto__switch":
                        try:
                            n = val.currentText()
                            s = self.main__layout.parentWidget().findChildren(QComboBox, 'id__shield')[0].currentText()
                            sql__id = f"SELECT id FROM auto__switch WHERE id__shield='{s}' AND name='{n}'"
                            res__sql_id = self.sqlite__cursor.execute(sql__id).fetchall()
                            self.save__param.setdefault(f'{val.objectName()}', res__sql_id[0][0])
                        except sqlite3.Error as err:
                            print(err)
                    else:
                        self.save__param.setdefault(f'{val.objectName()}', val.currentText())
                for val in param1:
                    if val.objectName() != '':
                        self.save__param.setdefault(f'{val.objectName()}', val.text())
                        val.clear()
                    else:
                        val.clear()
                if self.type == 'lighting':
                    self.save__param.setdefault(f'{spin[1].objectName()}', spin[1].value())
                    if q == 1:
                        keys = list(self.save__param.keys())
                        values = list(self.save__param.values())
                        result__value = ''
                        for v in values:
                            result__value = result__value + f"'{v}', "
                        result__value = result__value[:-2]
                        keys = ', '.join(keys)
                        self.sql__save = f"INSERT INTO {self.type}({keys}) VALUES({result__value})"
                        try:
                            self.sqlite__cursor.execute(self.sql__save)
                        except sqlite3.Error as err:
                            print(err)
                    else:
                        temp__get_name = self.save__param.get('name')
                        for i in range(q):
                            temp__name = f"{temp__get_name}-{i+1}"
                            self.save__param['name'] = temp__name
                            keys = list(self.save__param.keys())
                            values = list(self.save__param.values())
                            result__value = ''
                            for v in values:
                                result__value = result__value + f"'{v}', "
                            result__value = result__value[:-2]
                            keys = ', '.join(keys)
                            self.sql__save = f"INSERT INTO {self.type}({keys}) VALUES({result__value})"
                            try:
                                self.sqlite__cursor.execute(self.sql__save)
                            except sqlite3.Error as err:
                                print(err)
                    self.sqlite__connect.commit()
                else:
                    keys = list(self.save__param.keys())
                    values = list(self.save__param.values())
                    result__value = ''
                    for v in values:
                        result__value = result__value + f"'{v}', "
                    result__value = result__value[:-2]
                    keys = ', '.join(keys)
                    self.sql__save = f"INSERT INTO {self.type}({keys}) VALUES({result__value})"
                    try:
                        self.sqlite__cursor.execute(self.sql__save)
                        self.sqlite__connect.commit()
                    except sqlite3.Error as err:
                        print(err)
            else:
                # name.setFocus()
                pass

    def closed(self):
        self.accept()