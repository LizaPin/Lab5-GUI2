import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QPushButton, QHBoxLayout, QMessageBox, QMenuBar, QAction, QMainWindow, QFileDialog, QCalendarWidget, \
    QDialog, QTabWidget, QLabel, QLineEdit, QInputDialog
from PyQt5.QtGui import QIcon
import pandas as pd
import matplotlib.pyplot as plt
from util import splitting_x_y, date_search, splitting_week, splitting_year, create_annotation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = None  # Хранение текущего датасета
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #DDA0DD;")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Меню
        menubar = self.menuBar()
        menubar.setStyleSheet("background-color: #8A2BE2; color: white;")
        file_menu = menubar.addMenu('Файл')

        self.file_action_open = QAction('Открыть', self)
        self.file_action_open.triggered.connect(self.on_file_open_click)
        file_menu.addAction(self.file_action_open)

        self.file_action_annotation = QAction('Создать аннотацию', self)
        self.file_action_annotation.setEnabled(False)
        self.file_action_annotation.triggered.connect(self.on_annotation_click)
        file_menu.addAction(self.file_action_annotation)

        # Вкладки
        self.tabs = QTabWidget(self)
        layout.addWidget(self.tabs)

        # Создаем вкладки
        self.processing_tab = QWidget()
        self.analysis_tab = QWidget()
        self.tabs.addTab(self.processing_tab, "Обработка данных")
        self.tabs.addTab(self.analysis_tab, "Анализ данных")

        self.init_processing_tab()
        self.init_analysis_tab()

        self.setWindowTitle('Работа с данными')
        self.setGeometry(400, 400, 800, 600)
        self.show()

    def init_processing_tab(self):
        layout = QVBoxLayout(self.processing_tab)

        # Таблица для отображения данных
        self.table_processing = QTableWidget()
        self.table_processing.setStyleSheet("background-color: white; color: black;")
        layout.addWidget(self.table_processing)

        # Кнопки для обработки данных
        button_layout = QHBoxLayout()

        self.buttonFindValue = QPushButton('Получить данные')
        self.buttonFindValue.setEnabled(False)
        self.buttonFindValue.setStyleSheet("background-color: white; color: black;")
        button_layout.addWidget(self.buttonFindValue)

        self.buttonXY = QPushButton('Разделить на x и y')
        self.buttonXY.setEnabled(False)
        self.buttonXY.setStyleSheet("background-color: white; color: black;")
        button_layout.addWidget(self.buttonXY)

        self.buttonYearsSplit = QPushButton('Разделить по годам')
        self.buttonYearsSplit.setEnabled(False)
        self.buttonYearsSplit.setStyleSheet("background-color: white; color: black;")
        button_layout.addWidget(self.buttonYearsSplit)

        self.buttonWeeksSplit = QPushButton('Разделить по неделям')
        self.buttonWeeksSplit.setEnabled(False)
        self.buttonWeeksSplit.setStyleSheet("background-color: white; color: black;")
        button_layout.addWidget(self.buttonWeeksSplit)

        layout.addLayout(button_layout)

        # Привязываем функции к кнопкам
        self.buttonFindValue.clicked.connect(self.date_search)
        self.buttonXY.clicked.connect(self.splitting_x_y)
        self.buttonYearsSplit.clicked.connect(self.splitting_years)
        self.buttonWeeksSplit.clicked.connect(self.splitting_weeks)

    def init_analysis_tab(self):
        layout = QVBoxLayout(self.analysis_tab)

        # Таблица для анализа данных
        self.table_analysis = QTableWidget()
        self.table_analysis.setStyleSheet("background-color: white; color: black;")
        layout.addWidget(self.table_analysis)

        # Кнопки для анализа
        self.buttonFilter = QPushButton("Фильтр по отклонению")
        self.buttonFilter.setStyleSheet("background-color: white; color: black;")
        layout.addWidget(self.buttonFilter)

        self.buttonFullGraph = QPushButton("График за весь период")
        self.buttonFullGraph.setStyleSheet("background-color: white; color: black;")
        layout.addWidget(self.buttonFullGraph)

        self.buttonPeriodGraph = QPushButton("График по определенному периоду")
        self.buttonPeriodGraph.setStyleSheet("background-color: white; color: black;")
        layout.addWidget(self.buttonPeriodGraph)

        self.buttonMonthGraph = QPushButton("График за месяц")
        self.buttonMonthGraph.setStyleSheet("background-color: white; color: black;")
        layout.addWidget(self.buttonMonthGraph)

        # Обработчики событий
        self.buttonFilter.clicked.connect(self.filter_data)
        self.buttonFullGraph.clicked.connect(self.show_full_graph)
        self.buttonPeriodGraph.clicked.connect(self.show_period_graph)
        self.buttonMonthGraph.clicked.connect(self.show_month_graph)

    def on_file_open_click(self):
        self.datasetpaths = QFileDialog.getOpenFileNames(self, 'Выберите файл', filter="*.csv")[0]
        if not self.datasetpaths:
            return

        self.df = pd.read_csv(self.datasetpaths[0], sep=";")
        self.df.columns = ["date", "value"]
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df["deviation_from_median"] = self.df["value"] - self.df["value"].median()
        self.df["deviation_from_mean"] = self.df["value"] - self.df["value"].mean()

        # Заполняем таблицы
        self.fill_table(self.table_processing, self.df)
        self.fill_table(self.table_analysis, self.df, analysis=True)

        self.buttonFindValue.setEnabled(True)
        self.buttonXY.setEnabled(True)
        self.buttonYearsSplit.setEnabled(True)
        self.buttonWeeksSplit.setEnabled(True)
        self.file_action_annotation.setEnabled(True)

    def fill_table(self, table, data, analysis=False):
        table.setRowCount(0)
        table.setColumnCount(4 if analysis else 2)
        headers = ["Дата", "Стоимость"]
        if analysis:
            headers.extend(["Отклонение от медианы", "Отклонение от среднего"])
        table.setHorizontalHeaderLabels(headers)

        for i, row in data.iterrows():
            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem(str(row["date"])))
            table.setItem(i, 1, QTableWidgetItem(str(row["value"])))
            if analysis:
                table.setItem(i, 2, QTableWidgetItem(f"{row['deviation_from_median']:.2f}"))
                table.setItem(i, 3, QTableWidgetItem(f"{row['deviation_from_mean']:.2f}"))
        table.resizeColumnsToContents()

    def on_annotation_click(self):
        result_folder = QFileDialog.getExistingDirectory(self, caption='Выберите папку для файла аннотации')
        if not result_folder:
            QMessageBox.warning(self, "Ошибка", "Папка не выбрана!")
            return
        if create_annotation.create_annotation(self.datasetpaths[0], result_folder):
            QMessageBox.information(self, "Успех", "Файл аннотации создан!")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось создать аннотацию!")

    def date_search(self):
        selected_date = self.open_calendar()
        if selected_date:
            value = date_search.get_value(selected_date, self.datasetpaths)
            QMessageBox.information(self, "Результат", f"Значение: {value}" if value else "Нет данных за эту дату!")

    def open_calendar(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Выбор даты")
        layout = QVBoxLayout(dialog)
        calendar = QCalendarWidget(dialog)
        layout.addWidget(calendar)
        btn = QPushButton("Выбрать дату", dialog)
        layout.addWidget(btn)
        btn.clicked.connect(dialog.accept)
        if dialog.exec_() == QDialog.Accepted:
            return calendar.selectedDate().toString("yyyy-MM-dd")
        return None

    def splitting_x_y(self):
        result_folder = QFileDialog.getExistingDirectory(self, caption='Выберите папку для выходных файлов')
        if result_folder == "":
            QMessageBox.warning(self, "Ошибка", "Папка не выбрана!")
            return
        if splitting_x_y.splitting_x_y(filename=self.datasetpaths[0], x_file=result_folder + "/x.csv", y_file=result_folder + "/y.csv"):
            QMessageBox.information(self, "Успех", "Файлы созданы!")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось создать файлы!")

    def splitting_years(self):
        result_folder = QFileDialog.getExistingDirectory(self, caption='Выберите папку для выходных файлов')
        if result_folder == "":
            QMessageBox.warning(self, "Ошибка", "Папка не выбрана!")
            return
        if splitting_year.splitting_year(self.datasetpaths[0], result_folder):
            QMessageBox.information(self, "Успех", "Файлы по годам созданы!")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось разделить данные!")

    def splitting_weeks(self):
        result_folder = QFileDialog.getExistingDirectory(self, caption='Выберите папку для выходных файлов')
        if result_folder == "":
            QMessageBox.warning(self, "Ошибка", "Папка не выбрана!")
            return
        if splitting_week.splitting_week(self.datasetpaths[0], result_folder):
            QMessageBox.information(self, "Успех", "Файлы по неделям созданы!")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось разделить данные!")

    def filter_data(self):
        try:
            filter_value, ok = QInputDialog.getDouble(self, "Фильтр по отклонению", "Введите значение отклонения:", decimals=2)
            if ok:
                filtered_df = self.df[(abs(self.df["deviation_from_median"]) > filter_value) |
                                      (abs(self.df["deviation_from_mean"]) > filter_value)]
                self.fill_table(self.table_analysis, filtered_df, analysis=True)
            else:
                QMessageBox.information(self, "Отмена", "Фильтр не применён.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")

    def show_full_graph(self):
        plt.figure()
        plt.plot(self.df["date"], self.df["value"], label="Стоимость")
        plt.title("График за весь период")
        plt.xlabel("Дата")
        plt.ylabel("Стоимость")
        plt.legend()
        plt.grid()
        plt.show()

    def show_period_graph(self):
        start_date = self.open_calendar()
        end_date = self.open_calendar()
        if start_date and end_date:
            period_df = self.df[(self.df["date"] >= start_date) & (self.df["date"] <= end_date)]
            plt.figure()
            plt.plot(period_df["date"], period_df["value"], label="Стоимость")
            plt.title(f"График за период: {start_date} - {end_date}")
            plt.xlabel("Дата")
            plt.ylabel("Стоимость")
            plt.legend()
            plt.grid()
            plt.show()

    def show_month_graph(self):
        selected_date = self.open_calendar()
        if selected_date:
            selected_month = pd.to_datetime(selected_date).month
            selected_year = pd.to_datetime(selected_date).year
            month_df = self.df[(self.df["date"].dt.month == selected_month) & (self.df["date"].dt.year == selected_year)]
            median_value = month_df["value"].median()
            mean_value = month_df["value"].mean()

            plt.figure()
            plt.plot(month_df["date"], month_df["value"], label="Стоимость")
            plt.axhline(y=median_value, color='r', linestyle='--', label=f"Медиана: {median_value:.2f}")
            plt.axhline(y=mean_value, color='g', linestyle='--', label=f"Среднее: {mean_value:.2f}")
            plt.title(f"График за {selected_month}/{selected_year}")
            plt.xlabel("Дата")
            plt.ylabel("Стоимость")
            plt.legend()
            plt.grid()
            plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
