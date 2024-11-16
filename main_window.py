import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, \
QPushButton, QHBoxLayout, QMessageBox, QMenuBar, QAction, QMainWindow, QFileDialog, QCalendarWidget, \
QDialog
from PyQt5.QtGui import QIcon

from util import splitting_x_y, date_search, splitting_week, splitting_year, create_annotation

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Устанавливаем цвет фона для главного окна
        self.setStyleSheet("background-color: #DDA0DD;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Меню с фоном #8A2BE2
        menubar = self.menuBar()
        menubar.setStyleSheet("background-color: #8A2BE2; color: white;")
        
        file_menu = menubar.addMenu('Файл')
        self.file_action_open = QAction('Открыть', self)
        self.file_action_open.triggered.connect(self.on_file_open_click)
       
       # Панель инструментов с кнопкой "Создать аннотацию"
        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.setStyleSheet("background-color: #8A2BE2;")
        
        self.file_action_annotation = QAction('Создать аннотацию', self)
        self.file_action_annotation.setEnabled(False)
        self.file_action_annotation.setVisible(False)
        self.file_action_annotation.triggered.connect(self.on_annotation_click)
        self.toolbar.addAction(self.file_action_annotation)
       
        file_menu.addAction(self.file_action_open)
        file_menu.addAction(self.file_action_annotation)

        # Таблица будет белой
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Дата", "Стоимость"])
        self.table.setStyleSheet("background-color: white; color: black;")

        layout.addWidget(self.table)

        # Кнопки будут белыми и скрыты по умолчанию
        button_layout = QHBoxLayout()

        self.buttonFindValue = QPushButton('Получить данные')
        self.buttonXY = QPushButton('Разделить на x и y')
        self.buttonYearsSplit = QPushButton('Разделить по годам')
        self.buttonWeeksSplit = QPushButton('Разделить по неделям')

        # Изначально кнопки скрыты и не активны
        self.buttonFindValue.setEnabled(False)
        self.buttonXY.setEnabled(False)
        self.buttonYearsSplit.setEnabled(False)
        self.buttonWeeksSplit.setEnabled(False)

        # Устанавливаем стиль кнопок, чтобы они были белыми
        self.buttonFindValue.setStyleSheet("background-color: white; color: black;")
        self.buttonXY.setStyleSheet("background-color: white; color: black;")
        self.buttonYearsSplit.setStyleSheet("background-color: white; color: black;")
        self.buttonWeeksSplit.setStyleSheet("background-color: white; color: black;")

        # Скрываем кнопки
        self.buttonFindValue.setVisible(False)
        self.buttonXY.setVisible(False)
        self.buttonYearsSplit.setVisible(False)
        self.buttonWeeksSplit.setVisible(False)

        button_layout.addWidget(self.buttonFindValue)
        button_layout.addWidget(self.buttonXY)
        button_layout.addWidget(self.buttonYearsSplit)
        button_layout.addWidget(self.buttonWeeksSplit)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.setWindowTitle('оно работает работает')
        self.setGeometry(400, 400, 400, 400)
        self.show()

        self.buttonFindValue.clicked.connect(self.date_search)
        self.buttonXY.clicked.connect(self.splitting_x_y)
        self.buttonYearsSplit.clicked.connect(self.splitting_years)
        self.buttonWeeksSplit.clicked.connect(self.splitting_weeks)

    def on_file_open_click(self):
        self.datasetpaths = QFileDialog.getOpenFileNames(self, 'Выберите файл', filter="*.csv")[0]
        if len(self.datasetpaths) == 0:
            return
        
        # После того как файл выбран, показываем кнопки и активируем их
        self.buttonFindValue.setEnabled(True)
        self.buttonXY.setEnabled(True)
        self.buttonYearsSplit.setEnabled(True)
        self.buttonWeeksSplit.setEnabled(True)

        # Устанавливаем стиль кнопок, чтобы они были белыми
        self.buttonFindValue.setStyleSheet("background-color: white; color: black;")
        self.buttonXY.setStyleSheet("background-color: white; color: black;")
        self.buttonYearsSplit.setStyleSheet("background-color: white; color: black;")
        self.buttonWeeksSplit.setStyleSheet("background-color: white; color: black;")

        # Показываем кнопки
        self.buttonFindValue.setVisible(True)
        self.buttonXY.setVisible(True)
        self.buttonYearsSplit.setVisible(True)
        self.buttonWeeksSplit.setVisible(True)

        i = 0
        for index, line in date_search.DataFrameIterator(date_search.create_dataset_from_files(self.datasetpaths)):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(line.iloc[0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(line.iloc[1])))
            i += 1
        
        self.file_action_annotation.setEnabled(True)
        self.file_action_annotation.setVisible(True)
        
    def on_annotation_click(self):
        result_folder = QFileDialog.getExistingDirectory(self, caption='Выберите папку для файла аннотации')
        if result_folder == "":
            QMessageBox.information(self, "Ошибка!", "Вы не выбрали папку")
            return
        if create_annotation.create_annotation(filename=self.datasetpaths[0], result_folder=result_folder):
            QMessageBox.information(self, "Успех", "Файл создан")
        else:
            QMessageBox.information(self, "Ошибка!", "Что-то пошло не так!")

    def date_search(self):
        selected_date = self.open_calendar()
        if selected_date is not None:
            result = date_search.get_value(selected_date, self.datasetpaths)
            if result is not None:
                QMessageBox.information(self, "Значение найдено", f"Значение {selected_date} было равно {result}")
            else:
                QMessageBox.information(self, "Значение не найдено!", "Значения за эту дату нет!")
        else:
            QMessageBox.warning(self, "Ошибка", "Дата не была выбрана")

    def open_calendar(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Выбор даты')
        dialog.setGeometry(300, 300, 300, 250)

        layout = QVBoxLayout(dialog)

        calendar = QCalendarWidget(dialog)
        layout.addWidget(calendar)

        btn_select = QPushButton('Выбрать дату', dialog)
        layout.addWidget(btn_select)

        selected_date = None

        def select_date():
            nonlocal selected_date
            selected_qdate = calendar.selectedDate()
            selected_date = selected_qdate.toString("yyyy-MM-dd")
            dialog.accept()

        btn_select.clicked.connect(select_date)

        if dialog.exec_() == QDialog.Accepted:
            return selected_date  

        return None

    def splitting_x_y(self):
        result_folder = QFileDialog.getExistingDirectory(self, caption='Выберите папку для выходных файлов')
        if result_folder == "":
            QMessageBox.information(self, "Ошибка!", "Вы не выбрали папку")
            return
        if splitting_x_y.splitting_x_y(filename=self.datasetpaths[0], x_file=result_folder + "/x.csv", y_file=result_folder + "/y.csv"):
            QMessageBox.information(self, "Успех", "Файлы созданы")
        else:
            QMessageBox.information(self, "Ошибка!", "Что-то пошло не так!")

    def splitting_years(self):
        result_folder = QFileDialog.getExistingDirectory(self, caption='Выберите папку для выходных файлов')
        if result_folder == "":
            QMessageBox.information(self, "Ошибка!", "Вы не выбрали папку")
            return
        if splitting_year.splitting_year(filename=self.datasetpaths[0], result_folder=result_folder):
            QMessageBox.information(self, "Успех", "Файлы созданы")
        else:
            QMessageBox.information(self, "Ошибка!", "Что-то пошло не так!")

    def splitting_weeks(self):
        result_folder = QFileDialog.getExistingDirectory(self, caption='Выберите папку для выходных файлов')
        if result_folder == "":
            QMessageBox.information(self, "Ошибка!", "Вы не выбрали папку")
            return
        if splitting_week.splitting_week(filename=self.datasetpaths[0], result_folder=result_folder):
            QMessageBox.information(self, "Успех", "Файлы созданы")
        else:
            QMessageBox.information(self, "Ошибка!", "Что-то пошло не так!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
