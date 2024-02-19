import sqlite3
from PyQt6.QtWidgets import (QComboBox, QDialog,
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFrame)


class EquipmentChange(QDialog):
    def __init__(self, parent=None, sqlite__connect=None, sqlite__cursor=None, equipment__type=None, characteristics__to=None, value=None):
        super().__init__(parent)
        self.setWindowTitle("Изменить оборудование")
        self.window().adjustSize()
        self.setMinimumWidth(240)
        self.setMaximumWidth(300)
        self.sqlite__connect = sqlite__connect
        self.sqlite__cursor = sqlite__cursor
        self.equipment__type = equipment__type
        self.characteristics__to = characteristics__to
        self.value__change = value
        self.name__old = ''
        self.id = ''
        self.transformer__old = ''
        self.shield__old = ''
        self.switch__shield_old = ''
        self.room__old = ''
        self.UI()
    def UI(self):

        self.v__layout = QVBoxLayout(self)
        param = self.find__unit_change()
        temp__type_index = ''
        for key, value in param.items():
            if key != "id":
                if self.value__change[0] == 'auto__switch' and key == 'id__auto_switch':
                    self.v__layout.addWidget(QLabel(f"Запитан от:"))
                elif key == 'nominal__voltage' and self.value__change[0] == 'electric__motor':
                    self.v__layout.addWidget(QLabel('Напрежение, ток, скорость'))
                elif key == 'nominal__current' and self.value__change[0] == 'electric__motor':
                    pass
                elif key == 'nominal__speed' and self.value__change[0] == 'electric__motor':
                    pass
                elif key == 'weight' and self.value__change[0] == 'electric__motor':
                    self.v__layout.addWidget(QLabel('Вес, габариты'))
                elif key == 'size' and self.value__change[0] == 'electric__motor':
                    pass
                else:
                    self.v__layout.addWidget(QLabel(f"{self.characteristics__to[key]}"))
                if key == 'id__room':
                    if self.value__change[0] == 'rooms':
                        self.room__old = value
                        self.line__edit = QLineEdit()
                        self.line__edit.setObjectName(f"{key}")
                        self.line__edit.setText(f"{value}")
                        self.v__layout.addWidget(self.line__edit)
                    else:
                        self.combobox = QComboBox()
                        self.combobox.setObjectName(f"{key}")
                        self.combobox.clear()
                        val = self.get__value(key)
                        self.combobox.addItem(f"{value}")
                        for i in range(len(val)):
                            self.combobox.addItem(val[i][0])
                        self.combobox.setCurrentText(f"{value}")
                        if self.value__change[0] == 'rooms':
                            self.combobox.setEditable(True)
                            self.combobox.setEnabled(False)
                        self.v__layout.addWidget(self.combobox)
                elif key == 'id__transformer':
                    self.transformer__old = value
                    self.line__edit = QLineEdit()
                    self.line__edit.setObjectName(f"{key}")
                    self.line__edit.setText(f"{value}")
                    self.v__layout.addWidget(self.line__edit)
                    # self.combobox = QComboBox()
                    # self.combobox.setObjectName(f"{key}")
                    # self.combobox.clear()
                    # val = self.get__value(key)
                    # for i in range(len(val)):
                    #     self.combobox.addItem(val[i][0])
                    # self.combobox.setCurrentText(f"{value}")
                    # if self.value__change[0] == 'transformer':
                    #     self.combobox.setEnabled(False)
                    # self.v__layout.addWidget(self.combobox)
                elif key == 'id__shield' and self.value__change[0] == 'shield':
                    self.shield__old = value
                    self.line__edit = QLineEdit()
                    self.line__edit.setObjectName(f"{key}")
                    self.line__edit.setText(f"{value}")
                    self.v__layout.addWidget(self.line__edit)
                elif key == 'id__shield':
                    if self.value__change[0] == 'auto__switch':
                        self.switch__shield_old = value
                    self.combobox = QComboBox()
                    self.combobox.setObjectName(f"{key}")
                    self.combobox.clear()
                    val = self.get__value(key)
                    for i in range(len(val)):
                        self.combobox.addItem(val[i][0])
                    self.combobox.setCurrentText(f"{value}")
                    if self.value__change[0] != 'auto__switch' and self.value__change[0] != 'shield':
                        self.combobox.currentTextChanged.connect(lambda val=self.combobox.currentText(): self.reload__auto_switch(val))
                    if self.value__change[0] == 'shield':
                        self.combobox.setEnabled(False)
                    self.v__layout.addWidget(self.combobox)
                elif self.value__change[0] == 'auto__switch' and key == 'type':
                    self.combobox = QComboBox()
                    self.combobox.setObjectName(f"{key}")
                    self.combobox.clear()
                    type = ['Диф', 'Узо', 'Автомат', 'Рубильник']
                    self.combobox.addItems(type)
                    self.combobox.setCurrentText(f"{value}")
                    self.combobox.currentIndexChanged.connect(lambda x=self.combobox.currentIndex(): self.type__on_off(x))
                    temp__type_index = self.combobox.currentIndex()
                    self.v__layout.addWidget(self.combobox)
                elif key == 'id__auto_switch' and self.value__change[0] != 'auto__switch':
                    self.combobox = QComboBox()
                    self.combobox.setObjectName(f"{key}")
                    self.combobox.clear()
                    val = self.get__value(key, self.v__layout.parentWidget().findChild(QComboBox, 'id__shield').currentText())
                    for i in range(len(val)):
                        self.combobox.addItem(val[i][1])
                    temp = value.split(',')
                    if len(temp) > 1:
                        self.combobox.setCurrentText(f"{temp[1].strip()}")
                    self.v__layout.addWidget(self.combobox)
                elif key == 'id__auto_switch' and self.value__change[0] == 'auto__switch':
                    self.combobox = QComboBox()
                    self.combobox.setObjectName(f"{key}")
                    self.combobox.clear()
                    self.combobox.addItem(value)
                    self.combobox.setEditable(True)
                    self.combobox.currentTextChanged.connect(lambda text=self.combobox.currentText(): self.find__powered_from(text))
                    self.v__layout.addWidget(self.combobox)
                elif self.value__change[0] == 'electric__motor' and key == 'nominal__voltage':
                    self.electric__motor_frame = QFrame()
                    self.electric__motor_frame_hlayout = QHBoxLayout()
                    self.electric__motor_frame_hlayout.setContentsMargins(0, 0, 0, 0)
                    self.electro__motor_comboBox = QComboBox()
                    self.electro__motor_comboBox.setObjectName(f'{key}')
                    self.electro__motor_comboBox.setMinimumWidth(80)
                    self.electro__motor_comboBox.addItem('220')
                    self.electro__motor_comboBox.addItem('380')
                    self.electro__motor_comboBox.setCurrentText(f"{value}")
                    self.electric__motor_frame_hlayout.addWidget(self.electro__motor_comboBox)
                    self.line__edit_current = QLineEdit()
                    self.line__edit_current.setObjectName('nominal__current')
                    self.line__edit_current.setMinimumWidth(80)
                    self.electric__motor_frame_hlayout.addWidget(self.line__edit_current)
                    self.line__edit_speed = QLineEdit()
                    self.line__edit_speed.setObjectName('nominal__speed')
                    self.line__edit_speed.setMinimumWidth(80)
                    self.electric__motor_frame_hlayout.addWidget(self.line__edit_speed)
                    self.electric__motor_frame.setLayout(self.electric__motor_frame_hlayout)
                    self.v__layout.addWidget(self.electric__motor_frame)
                elif self.value__change[0] == 'electric__motor' and key == 'nominal__current':
                    self.line__edit_current.setText(f"{value}")
                elif self.value__change[0] == 'electric__motor' and key == 'nominal__speed':
                    self.line__edit_speed.setText(f"{value}")
                elif self.value__change[0] == 'electric__motor' and key == 'weight':
                    self.electric__motor_frame = QFrame()
                    self.electric__motor_frame_hlayout = QHBoxLayout()
                    self.electric__motor_frame_hlayout.setContentsMargins(0, 0, 0, 0)
                    self.line__edit_weight = QLineEdit()
                    self.line__edit_weight.setObjectName('weight')
                    self.line__edit_weight.setMinimumWidth(70)
                    self.line__edit_weight.setText(f"{value}")
                    self.electric__motor_frame_hlayout.addWidget(self.line__edit_weight)
                    self.line__edit_size = QLineEdit()
                    self.line__edit_size.setObjectName('size')
                    self.line__edit_size.setMinimumWidth(70)
                    self.electric__motor_frame_hlayout.addWidget(self.line__edit_size)
                    self.electric__motor_frame.setLayout(self.electric__motor_frame_hlayout)
                    self.v__layout.addWidget(self.electric__motor_frame)
                elif self.value__change[0] == 'electric__motor' and key == 'size':
                    self.line__edit_size.setText(f"{value}")
                elif self.value__change[0] == 'electric__motor' and key == 'motor__starting_method':
                    self.combobox = QComboBox()
                    self.combobox.setObjectName(f'{key}')
                    self.combobox.addItem('Треугольник')
                    self.combobox.addItem('Звезда')
                    self.combobox.setCurrentText(f"{value}")
                    self.v__layout.addWidget(self.combobox)
                else:
                    # if self.value__change[0] == 'auto__switch' and key == 'name':
                    if key == 'name':
                        self.name__old = value
                    self.line__edit = QLineEdit()
                    self.line__edit.setObjectName(f"{key}")
                    self.line__edit.setText(f"{value}")
                    self.v__layout.addWidget(self.line__edit)
        self.btn__change = QPushButton("Изменить")
        self.btn__change.setStyleSheet("margin-top: 10px")
        self.btn__change.clicked.connect(lambda : self.change__save())
        self.v__layout.addWidget(self.btn__change)
        self.find__line_edit = self.v__layout.parentWidget().findChildren(QLineEdit)
        self.find__combo_box = self.v__layout.parentWidget().findChildren(QComboBox)
        if self.value__change[0] == 'auto__switch':
            self.type__on_off(temp__type_index)

    def change__save(self):
        items = [qWid for qWid in self.findChildren(QWidget)]
        table = self.value__change[0]
        temp__shield = ''
        temp__room = ''
        temp__transformer = ''
        temp__name = ''
        update = ''
        tabl = ''
        for i in items:
            match i.metaObject().className():
                case 'QComboBox':
                    if i.currentText() == '':
                        i.setFocus()
                        return
                    match i.objectName():
                        case 'id__shield':
                            id__shield = i
                            temp__shield = id__shield.currentText().strip()
                    if i.objectName() == 'id__auto_switch' and table == 'auto__switch':
                        t = i.currentText().strip().split(',')
                        if len(t) == 1:
                            tr = t[0].strip()
                            res = self.sqlite__cursor.execute(f"SELECT id__transformer FROM transformer WHERE id__transformer='{tr}'").fetchone()
                            if res:
                                update = update + f"{i.objectName()}='{tr}',"
                            else:
                                i.setFocus()
                                return
                        else:
                            sh, sw = t[0].strip(), t[1].strip()
                            res = self.sqlite__cursor.execute(f"SELECT id FROM auto__switch WHERE id__shield='{sh}' AND name='{sw}'").fetchone()[0]
                            update = update + f"{i.objectName()}='{res}',"
                    else:
                        if i.objectName() == 'id__auto_switch':
                            try:
                                res = self.sqlite__cursor.execute(
                                    f"SELECT id FROM auto__switch WHERE id__shield='{temp__shield}' AND name='{i.currentText().strip()}'").fetchone()[0]
                                update = update + f"{i.objectName()}='{res}',"
                            except sqlite3.Error as err:
                                print(err)
                        else:
                            update = update + f"{i.objectName()}='{i.currentText().strip()}',"
                    # colums = colums + f"{i.objectName()},"
                    # colums__value = colums__value + f"{i.currentText().strip()},"

                        # case 'id__transformer':
                        #     id__transformer = i
                        #     temp__transformer = id__transformer.currentText().strip()
                        # case 'id__room':
                        #     id__room = i
                        #     temp__room = id__room.currentText().strip()
                case 'QLineEdit':
                    if i.text() == '':
                        i.setFocus()
                        return
                    if i.objectName() != '':
                        update = update + f"{i.objectName()}='{i.text().strip()}',"
                    if i.objectName() == 'name':
                        name = i
                        temp__name = name.text().strip()
                    if i.objectName() == 'id__room':
                        id__room = i
                        temp__room = id__room.text().strip()
                    if i.objectName() == 'id__transformer':
                        id__transformer = i
                        temp__transformer = id__transformer.text().strip()
                    if i.objectName() == 'id__shield':
                        id__shield = i
                        temp__shield = id__shield.text().strip()
        update = update[:-1]
        match table:
            case 'auto__switch':
                usl = int(self.sqlite__cursor.execute(f"SELECT EXISTS(SELECT * FROM auto__switch WHERE id__shield='{temp__shield}' AND name='{temp__name}')").fetchone()[0])
                if usl == 0 or (usl == 1 and temp__name == self.name__old and temp__shield == self.switch__shield_old):
                    sql__update = f"UPDATE auto__switch SET {update} WHERE id='{self.id}'"
                    try:
                        self.sqlite__cursor.execute(sql__update)
                        self.sqlite__connect.commit()
                    except sqlite3.Error as err:
                        print(err)
                else:
                    name.setFocus()
                    return
            case 'cable':
                usl = int(self.sqlite__cursor.execute(f"SELECT EXISTS(SELECT name FROM cable WHERE name='{temp__name}')").fetchone()[0])
                if usl == 1:
                    sql__update = f"UPDATE {table} SET {update} WHERE id='{self.id}'"
                    try:
                        self.sqlite__cursor.execute(sql__update)
                        self.sqlite__connect.commit()
                    except sqlite3.Error as err:
                        print(err)
                else:
                    name.setFocus()
                    return
            case 'rooms':
                tabl = self.equipment__type.copy()
                keys = ['rooms', 'cable', 'auto__switch']
                for key in keys:
                    tabl.pop(key, None)
                usl = int(self.sqlite__cursor.execute(f"SELECT EXISTS(SELECT id__room FROM rooms WHERE id__room='{self.room__old}')").fetchone()[0])
                if usl == 1:
                    sql__update = f"UPDATE {table} SET {update} WHERE id__room='{self.id}'"
                    try:
                        for t in tabl:
                            sql__update_table = f"UPDATE {t} SET id__room='{temp__room}' " \
                                          f"WHERE id__room='{self.room__old}'"
                            self.sqlite__cursor.execute(sql__update_table)
                        self.sqlite__cursor.execute(sql__update)
                        self.sqlite__connect.commit()
                    except sqlite3.Error as err:
                        print(err)
                else:
                    id__room.setFocus()
                    return
            case 'shield':
                tabl = self.equipment__type.copy()
                keys = ['rooms', 'shield', 'transformer']
                for key in keys:
                    tabl.pop(key, None)
                usl = int(self.sqlite__cursor.execute(f"SELECT EXISTS(SELECT id__shield FROM shield WHERE id__shield='{self.shield__old}')").fetchone()[0])
                if usl == 1:
                    sql__update = f"UPDATE {table} SET {update} WHERE id__shield='{self.id}'"
                    try:
                        for t in tabl:
                            self.sqlite__cursor.execute(f"UPDATE {t} SET id__shield='{temp__shield}' WHERE id__shield='{self.shield__old}'")
                        self.sqlite__cursor.execute(sql__update)
                        self.sqlite__connect.commit()
                    except sqlite3.Error as err:
                        print(err)
                else:
                    id__shield.setFocus()
                    return
            case 'transformer':
                tabl = self.equipment__type.copy()
                keys = ['rooms', 'shield', 'transformer']
                for key in keys:
                    tabl.pop(key, None)
                usl = int(self.sqlite__cursor.execute(f"SELECT EXISTS(SELECT id__transformer FROM transformer WHERE id__transformer='{self.transformer__old}')").fetchone()[0])
                if usl == 1:
                    sql__update = f"UPDATE {table} SET {update} WHERE id__transformer='{self.id}'"
                    try:
                        for t in tabl:
                            sql__update_transformer = f"UPDATE {t} SET id__auto_switch='{temp__transformer}' WHERE id__auto_switch='{self.transformer__old}'"
                            self.sqlite__cursor.execute(sql__update_transformer)
                        self.sqlite__cursor.execute(sql__update)
                        self.sqlite__connect.commit()
                    except sqlite3.Error as err:
                        print(err)
                else:
                    id__transformer.setFocus()
                    return
            case _:
                usl = int(self.sqlite__cursor.execute(f"SELECT EXISTS(SELECT * FROM {table} WHERE name='{temp__name}' AND id__room='{temp__room}')").fetchone()[0])
                if usl == 0 or (
                        usl == 1 and temp__name == self.name__old and temp__room == self.room__old):
                    sql__update = f"UPDATE {table} SET {update} WHERE id='{self.id}'"
                    try:
                        self.sqlite__cursor.execute(sql__update)
                        self.sqlite__connect.commit()
                    except sqlite3.Error as err:
                        print(err)
                else:
                    name.setFocus()
                    return
        self.accept()

    def find__powered_from(self, text):
        # t = ''.join(text.split())
        val = text.split(',')
        val1 = ''
        val2 = ''
        sql__select = ''
        if len(val) > 1:
            val1 = val[0].strip()
            val2 = val[1].strip()
            sql__select = f"SELECT DISTINCT * FROM auto__switch WHERE id__shield='{val1}' AND name LIKE '{val2}%' ORDER BY id__shield, name"
        elif val[0] == '':
            sql__select = ''
        else:
            val1 = val[0].strip()
            sql__select = f"SELECT DISTINCT * FROM auto__switch WHERE id__shield LIKE '{val1}%' ORDER BY id__shield, name"
        try:
            if sql__select != '':
                res = self.sqlite__cursor.execute(sql__select).fetchall()
            else:
                res = ''
            self.sender().blockSignals(True)
            self.sender().clear()
            self.sender().addItem(f'{text}')
            if res:
                for v in res:
                    self.sender().addItem(f'{v[8]}, {v[1]}')
            else:
                if text != '':
                    sql__select = f"SELECT DISTINCT id__transformer FROM transformer"
                    res = self.sqlite__cursor.execute(sql__select).fetchall()
                    self.sender().clear()
                    self.sender().addItem(f'{text}')
                    for v in res:
                        self.sender().addItem(f'{v[0]}')
            self.sender().blockSignals(False)
        except sqlite3.Error as err:
            print(err)

    def type__on_off(self, x):
        obj = {}
        for name in self.find__line_edit:
            obj[f"{format(name.objectName())}"] = name
        cutoff__current = obj['cutoff__current']
        leakage__current = obj['leakage__current']
        characteristic = obj['characteristic']
        cutoff__current_value = cutoff__current.text()
        leakage__current_value = leakage__current.text()
        characteristic__value = characteristic.text()
        match x:
            case 0:
                cutoff__current.setEnabled(True)
                leakage__current.setEnabled(True)
                characteristic.setEnabled(True)
                characteristic.setText(characteristic__value)
                cutoff__current.setText(cutoff__current_value)
                leakage__current.setText(leakage__current_value)
            case 1:
                characteristic.setEnabled(False)
                characteristic.setText('none')
                cutoff__current.setEnabled(True)
                cutoff__current.setText(cutoff__current_value)
                leakage__current.setEnabled(True)
                leakage__current.setText(leakage__current_value)
            case 2:
                characteristic.setEnabled(True)
                characteristic.setText(characteristic__value)
                leakage__current.setEnabled(False)
                leakage__current.setText('none')
                cutoff__current.setEnabled(True)
                cutoff__current.setText(cutoff__current_value)
            case 3:
                characteristic.setEnabled(False)
                characteristic.setText('none')
                cutoff__current.setEnabled(True)
                cutoff__current.setText(cutoff__current_value)
                leakage__current.setEnabled(False)
                leakage__current.setText('none')



    def find__unit_change(self):
        param = {}
        res = ''
        table__info = self.sqlite__cursor.execute(f"pragma table_info({self.value__change[0]})").fetchall()
        if len(self.value__change) == 2:
            if self.value__change[0] == 'rooms':
                res = self.sqlite__cursor.execute(f"SELECT * FROM rooms WHERE id__room='{self.value__change[1]}'").fetchall()
                self.id = res[0][0]
            elif self.value__change[0] == 'shield':
                res = self.sqlite__cursor.execute(f"SELECT * FROM shield WHERE id__shield='{self.value__change[1]}'").fetchall()
                self.id = res[0][0]
            elif self.value__change[0] == 'cable':
                res = self.sqlite__cursor.execute(f"SELECT * FROM cable WHERE name='{self.value__change[1]}'").fetchall()
                self.id = res[0][0]
        else:
            if self.value__change[0] == 'auto__switch':
                res = self.sqlite__cursor.execute(f"SELECT * FROM auto__switch WHERE id__shield='{self.value__change[1]}' AND name='{self.value__change[2]}'").fetchall()
                self.id = res[0][0]
            elif self.value__change[0] == 'transformer':
                res = self.sqlite__cursor.execute(f"SELECT * FROM {self.value__change[0]} WHERE id__transformer='{self.value__change[2]}' AND id__room='{self.value__change[1]}'").fetchall()
                self.id = res[0][0]
            elif self.value__change[0] == 'lighting':
                res = self.sqlite__cursor.execute(f"SELECT * FROM {self.value__change[0]} WHERE id='{self.value__change[2]}' AND id__room='{self.value__change[1]}'").fetchall()
                self.id = res[0][0]
            else:
                res = self.sqlite__cursor.execute(f"SELECT * FROM {self.value__change[0]} WHERE name='{self.value__change[2]}' AND id__room='{self.value__change[1]}'").fetchall()
                self.id = res[0][0]
        for i in range(len(table__info)):
            if table__info[i][1] == "id__auto_switch":
                val__switch_name = self.sqlite__cursor.execute(f"SELECT name, id__shield FROM auto__switch WHERE id='{res[0][i]}'").fetchall()
                if val__switch_name:
                    param[f"{table__info[i][1]}"] = f"{val__switch_name[0][1]}, {val__switch_name[0][0]}"
                elif not val__switch_name:
                    energized = self.sqlite__cursor.execute(
                        f"SELECT id__transformer FROM transformer WHERE id__transformer='{res[0][i]}'").fetchone()
                    if energized:
                        param[f"{table__info[i][1]}"] = energized[0]
                    else:
                        param[f"{table__info[i][1]}"] = 'none'
            else:
                param[f"{table__info[i][1]}"] = res[0][i]
        return param

    def get__value(self, key1, key2=None):
        k = key1
        try:
            if k == 'id__room':
                sql__select = f"SELECT id__room FROM rooms"
                return self.sqlite__cursor.execute(sql__select).fetchall()
            elif k == 'id__shield':
                sql__select = f"SELECT id__shield FROM shield"
                return self.sqlite__cursor.execute(sql__select).fetchall()
            elif k == 'id__auto_switch':
                sql__select = f"SELECT id, name FROM auto__switch WHERE id__shield='{key2}'"
                return self.sqlite__cursor.execute(sql__select).fetchall()
            elif k == 'id__transformer':
                sql__select = f"SELECT id__transformer FROM transformer"
                return self.sqlite__cursor.execute(sql__select).fetchall()
        except sqlite3.Error as err:
            print(err)

    def reload__auto_switch(self, key):
        try:
            sql__select = f"SELECT id, name FROM auto__switch WHERE id__shield='{key}'"
            res = self.sqlite__cursor.execute(sql__select).fetchall()
            re = self.v__layout.parentWidget().findChild(QComboBox, 'id__auto_switch')
            re.clear()
            for i in range(len(res)):
                re.addItem(res[i][1])
        except sqlite3.Error as err:
            print(err)

    def closed(self):
        self.accept()