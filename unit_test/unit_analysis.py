import unittest
import pandas as pd
from io import StringIO
from unittest.mock import patch
import io
import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импортируем ваши функции из модуля
from util.data_analysis import create_period, create_month, filter_date, filter_by_deviation, calculate_month

class TestFunctions(unittest.TestCase):
    
    def setUp(self):
        # Создаем тестовые данные
        self.data = """date;value
        2024-01-01;75.5
        2024-01-02;76.0
        2024-01-03;74.8
        2024-01-04;76.5
        2024-01-05;75.2
        """
        self.df = pd.read_csv(StringIO(self.data), sep=";")
        self.df['date'] = pd.to_datetime(self.df['date'])

    # Тест позитивного сценария для filter_date
    def test_filter_date_positive(self):
        result = filter_date(self.df, "2024-01-02", "2024-01-04")
        self.assertEqual(len(result), 3)
        self.assertEqual(result['value'].iloc[0], 76.0)

    # Тест негативного сценария для filter_date (отсутствие данных)
    def test_filter_date_no_data(self):
        result = filter_date(self.df, "2025-01-01", "2025-01-31")
        self.assertTrue(result.empty)

    # Тест исключительной ситуации для filter_by_deviation (отсутствие нужного столбца)
    def test_filter_by_deviation_exception(self):
        with self.assertRaises(ValueError):
            filter_by_deviation(self.df, threshold=5.0)

    # Тест calculate_month для корректности средних значений
    def test_calculate_month(self):
        result = calculate_month(self.df)
        self.assertEqual(len(result), 1)  # Все данные в одном месяце
        self.assertAlmostEqual(result['value'].iloc[0], 75.6, places=1)

    # Тест позитивного сценария для create_period
    @patch('matplotlib.pyplot.show')
    def test_create_period(self, mock_show):
        try:
            create_period(self.df, "2024-01-01", "2024-01-05")
            mock_show.assert_called_once()  # Убедимся, что график пытается отобразиться
        except Exception as e:
            self.fail(f"create_period вызвал ошибку: {e}")

    # Тест позитивного сценария для create_month
    @patch('matplotlib.pyplot.show')
    def test_create_month_positive(self, mock_show):
        try:
            create_month(self.df, "2024-01")
            mock_show.assert_called_once()  # Убедимся, что график пытается отобразиться
        except Exception as e:
            self.fail(f"create_month вызвал ошибку: {e}")

    # Тест негативного сценария для create_month (несуществующий месяц)
    def test_create_month_no_data(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            create_month(self.df, "2025-01")
            self.assertIn("Данных за месяц 2025-01 нет.", fake_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
