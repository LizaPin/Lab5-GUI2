import unittest
import pandas as pd
import os
from io import StringIO
import sys
# Добавляем путь к корневой директории проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.date_search import DataFrameIterator, create_dataset_from_files, get_value  # Импортируем функции из вашего модуля


class TestDataFrameIterator(unittest.TestCase):
    def setUp(self):
        # Создаем DataFrame для тестов
        self.df = pd.DataFrame({
            'Date': ['2024-01-01', '2024-01-02'],
            'Value': [100, 200]
        })
        self.iterator = DataFrameIterator(self.df)

    def test_iteration(self):
        # Проверяем правильность итерации
        rows = list(self.iterator)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][1]['Date'], '2024-01-01')
        self.assertEqual(rows[1][1]['Value'], 200)

    def test_stop_iteration(self):
        # Проверяем, что StopIteration вызывается правильно
        iterator = iter(self.iterator)
        next(iterator)  # Первая строка
        next(iterator)  # Вторая строка
        with self.assertRaises(StopIteration):
            next(iterator)  # Больше строк нет

class TestCreateDatasetFromFiles(unittest.TestCase):
    def setUp(self):
        # Создаем временные файлы для тестов
        self.file1 = "test_file1.csv"
        self.file2 = "test_file2.csv"

        with open(self.file1, "w") as f:
            f.write("Date;Value\n2024-01-01;100\n2024-01-02;200\n")

        with open(self.file2, "w") as f:
            f.write("Value\n300\n400\n")

    def tearDown(self):
        # Удаляем временные файлы после тестов
        os.remove(self.file1)
        os.remove(self.file2)

    def test_single_file(self):
        # Проверяем, что один файл читается корректно
        df = create_dataset_from_files([self.file1])
        self.assertEqual(df.shape, (2, 2))
        self.assertEqual(df.iloc[0]['Value'], 100)

    def test_multiple_files(self):
        # Проверяем, что более двух файлов корректно объединяются по строкам
        df = create_dataset_from_files([self.file1, self.file1])
        self.assertEqual(df.shape, (4, 2))

class TestGetValue(unittest.TestCase):
    def setUp(self):
        # Создаем временный файл для тестов
        self.file = "test_file.csv"
        with open(self.file, "w") as f:
            f.write("Date;Value\n2024-01-01;100\n2024-01-02;200\n")

    def tearDown(self):
        # Удаляем временный файл после тестов
        os.remove(self.file)

    def test_get_existing_value(self):
        # Проверяем, что значение для существующей даты возвращается
        value = get_value("2024-01-01", [self.file])
        self.assertEqual(value, 100)

    def test_get_non_existing_value(self):
        # Проверяем, что возвращается None для несуществующей даты
        value = get_value("2024-01-03", [self.file])
        self.assertIsNone(value)

if __name__ == '__main__':
    unittest.main()
