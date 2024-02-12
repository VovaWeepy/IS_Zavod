import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTableView, QVBoxLayout, QWidget, QDialog, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import sqlite3


class TovarWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Таблица Tovar")
        self.setGeometry(915, 720, 1100, 600)

        # Создаем кнопки "Добавить" и "Удалить" в окне таблицы Tovar
        self.addButton = QPushButton("Добавить", self)
        self.deleteButton = QPushButton("Удалить", self)

        # Создаем модель таблицы и связываем ее с виджетом QTableView
        self.model = QSqlTableModel()
        self.model.setTable("Tovar")
        self.model.select()

        self.tableView = QTableView()
        self.tableView.setModel(self.model)

        # Создаем вертикальный контейнер и добавляем в него кнопки и виджет таблицы
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addWidget(self.tableView)

        self.setLayout(layout)

        # Подключаем сигналы кнопок к соответствующим методам
        self.addButton.clicked.connect(self.add_row)
        self.deleteButton.clicked.connect(self.delete_row)

    def add_row(self):
        # Логика добавления новой строки в таблицу Tovar
        rowCount = self.model.rowCount()
        self.model.insertRow(rowCount)

    def delete_row(self):
        # Получаем индексы выбранных строк
        indexes = self.tableView.selectedIndexes()

        if indexes:
            # Запрашиваем подтверждение удаления
            confirm = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить выбранные строки?",
                                           QMessageBox.Yes | QMessageBox.No)

            if confirm == QMessageBox.Yes:
                # Удаляем выбранные строки из модели
                for index in indexes:
                    self.model.removeRow(index.row())

                # Применяем изменения
                self.model.select()
        else:
            QMessageBox.warning(self, "Внимание", "Вы не выбрали строки для удаления.")


class ZakupWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Таблица Zakup")
        self.setGeometry(915, 720, 1100, 600)

        # Создаем кнопки "Добавить" и "Закупить"
        self.addButton = QPushButton("Добавить", self)
        self.zakupitButton = QPushButton("Закупить", self)

        # Создаем модель таблицы и связываем ее с виджетом QTableView
        self.model = QSqlTableModel()
        self.model.setTable("Zakup")
        self.model.select()

        self.tableView = QTableView()
        self.tableView.setModel(self.model)

        # Создаем вертикальный контейнер и добавляем в него кнопки и виджет таблицы
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.zakupitButton)
        layout.addWidget(self.tableView)

        self.setLayout(layout)

        # Подключаем сигналы кнопок к соответствующим методам
        self.addButton.clicked.connect(self.add_row)
        self.zakupitButton.clicked.connect(self.zakupit)

    def add_row(self):
        # Логика добавления новой строки в таблицу Zakup
        rowCount = self.model.rowCount()
        self.model.insertRow(rowCount)

    def zakupit(self):
        indexes = self.tableView.selectedIndexes()

        if indexes:
            row = indexes[0].row()
            column = indexes[0].column()
            value_str = self.model.data(self.model.index(row, column), Qt.DisplayRole)

            # Проверяем, что выбранная ячейка второго столбца
            if column == 1:
                Sklad_model = QSqlTableModel()
                Sklad_model.setTable("Sklad")
                Sklad_model.select()

                if row < Sklad_model.rowCount():
                    # Получаем текущее значение из таблицы Sklad
                    current_value_str = Sklad_model.data(Sklad_model.index(row, column), Qt.DisplayRole)
                    try:
                        # Преобразуем строки в числа
                        value = float(value_str)
                        current_value = float(current_value_str)
                        # Обновляем значение в таблице Sklad
                        if Sklad_model.setData(Sklad_model.index(row, column), value + current_value):
                            # Применяем изменения
                            Sklad_model.submitAll()
                            QMessageBox.information(self, "Успех", "Закупка произведена успешно.")
                        else:
                            QMessageBox.warning(self, "Ошибка", "Не удалось обновить данные в таблице Sklad.")
                    except ValueError:
                        QMessageBox.warning(self, "Ошибка", "Данные не являются числовыми.")
                else:
                    QMessageBox.warning(self, "Ошибка", "Нет соответствующей строки в таблице Sklad.")
            else:
                QMessageBox.warning(self, "Ошибка", "Выбранная ячейка не является вторым столбцом.")
        else:
            QMessageBox.warning(self, "Ошибка", "Вы не выбрали ячейку для закупки.")


class SkladWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Таблица Sklad")
        self.setGeometry(915, 720, 1100, 600)

        # Создаем модель таблицы и связываем ее с виджетом QTableView
        self.model = QSqlTableModel()
        self.model.setTable("Sklad")
        self.model.select()

        self.tableView = QTableView()
        self.tableView.setModel(self.model)

        # Создаем вертикальный контейнер и добавляем в него виджет таблицы
        layout = QVBoxLayout()
        layout.addWidget(self.tableView)

        self.setLayout(layout)


class ProizvodstvoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Таблица Proizvodstvo")
        self.setGeometry(915, 720, 1100, 600)

        # Создаем модель таблицы и связываем ее с виджетом QTableView
        self.model = QSqlTableModel()
        self.model.setTable("Proizvodstvo")
        self.model.select()

        self.tableView = QTableView()
        self.tableView.setModel(self.model)

        # Создаем кнопку "Произвести"
        self.produceButton = QPushButton("Произвести", self)
        self.produceButton.clicked.connect(self.produce_item)

        # Создаем вертикальный контейнер и добавляем в него виджет таблицы и кнопку
        layout = QVBoxLayout()
        layout.addWidget(self.tableView)
        layout.addWidget(self.produceButton)  # Добавляем кнопку в интерфейс

        self.setLayout(layout)

    def produce_item(self):
        # Получаем выбранную ячейку
        indexes = self.tableView.selectedIndexes()

        # Проверка, что выбрана хотя бы одна ячейка
        if indexes:
            index = indexes[0]  # Если возможно выбрать несколько ячеек, ограничимся первой
            row = index.row()
            column = index.column()

            # Проверяем, что выбранная ячейка второго столбца
            if column == 1:
                # Получаем текущее значение ячейки
                value_str = self.model.data(index, Qt.DisplayRole)

                # Очищаем строку от нечисловых символов и преобразуем в число
                try:
                    value = float(value_str.replace(",", ".").strip())  # Заменяем запятые на точки, если это формат десятичных чисел

                    # Получаем модель для таблицы "Товар"
                    Tovar_model = QSqlTableModel()
                    Tovar_model.setTable("Tovar")
                    Tovar_model.select()

                    # Проверяем, что строка существует в таблице "Товар"
                    if row < Tovar_model.rowCount():
                        # Получаем текущее значение из таблицы "Товар"
                        current_value_str = Tovar_model.data(Tovar_model.index(row, 1), Qt.DisplayRole)
                        current_value = float(
                            current_value_str.replace(",", ".").strip())  # Аналогичная замена запятых на точки

                        # Обновляем значение в таблице "Товар"
                        new_value = current_value + value
                        if Tovar_model.setData(Tovar_model.index(row, 1), new_value):
                            # Применяем изменения
                            Tovar_model.submitAll()
                            QMessageBox.information(self, "Успех", "Производство произведено успешно.")
                        else:
                            QMessageBox.warning(self, "Ошибка", "Не удалось обновить данные в таблице Товар.")
                    else:
                        QMessageBox.warning(self, "Ошибка", "Нет соответствующей строки в таблице Товар.")
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Данные не являются числовыми.")
            else:
                QMessageBox.warning(self, "Ошибка", "Выбранная ячейка не является вторым столбцом.")
        else:
            QMessageBox.warning(self, "Внимание", "Вы не выбрали ячейку.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Главное окно")
        self.setGeometry(800, 500, 1340, 920)

        # Создаем кнопки для открытия окон с таблицами
        self.button1 = QPushButton("Товар", self)
        self.button2 = QPushButton("Закупки", self)
        self.button3 = QPushButton("Склад", self)
        self.button4 = QPushButton("Производство", self)

        # Устанавливаем положение и размер кнопок
        self.button1.setGeometry(10, 10, 300, 100)
        self.button2.setGeometry(350, 10, 300, 100)
        self.button3.setGeometry(690, 10, 300, 100)
        self.button4.setGeometry(1030, 10, 300, 100)

        # Подключаем сигналы кнопок к соответствующим методам
        self.button1.clicked.connect(self.open_tovar_table)
        self.button2.clicked.connect(self.open_zakup_table)
        self.button3.clicked.connect(self.open_sklad_table)
        self.button4.clicked.connect(self.open_proizvodstvo_table)

    def open_tovar_table(self):
        tovarWindow = TovarWindow(self)
        tovarWindow.exec()

    def open_zakup_table(self):
        zakupWindow = ZakupWindow(self)
        zakupWindow.exec()

    def open_sklad_table(self):
        skladWindow = SkladWindow(self)
        skladWindow.exec()

    def open_proizvodstvo_table(self):
        proizvodstvoWindow = ProizvodstvoWindow(self)
        proizvodstvoWindow.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Подключаемся к базе данных
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("IS_Zavod.db")
    if not db.open():
        print("Не удалось подключиться к базе данных.")
        sys.exit(1)

    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
