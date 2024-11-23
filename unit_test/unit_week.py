import unittest
import os
import datetime
from io import StringIO
from unittest.mock import patch
import sys
# Добавляем путь к корневой директории проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.splitting_week import splitting_week


class TestSplittingWeek(unittest.TestCase):

    def setUp(self):
        """Setup the test environment."""
        self.test_file = './test_dataset.csv'
        self.result_folder = './test_results'
        self.invalid_file = './non_existent_file.csv'
        self.test_data = "date;value\n2024-01-01;100\n2024-01-03;105\n2024-01-07;110\n"
        
        # Create test dataset
        with open(self.test_file, 'w') as f:
            f.write(self.test_data)
    
    def tearDown(self):
        """Clean up the test environment."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.result_folder):
            for file in os.listdir(self.result_folder):
                os.remove(os.path.join(self.result_folder, file))
            os.rmdir(self.result_folder)

    def test_splitting_week_success(self):
        """Тест на успешное разделение данных по неделям."""
        result = splitting_week(filename=self.test_file, result_folder=self.result_folder)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.result_folder))
        # Check if at least one CSV file was created
        files = os.listdir(self.result_folder)
        self.assertGreater(len(files), 0)

    def test_splitting_week_invalid_file_format(self):
        """Тест на неправильный формат строки."""
        invalid_data = "2024-01-01,100\n2024-01-07,110\n"  # Wrong separator
        with open(self.test_file, 'w') as f:
            f.write(invalid_data)

        result = splitting_week(filename=self.test_file, result_folder=self.result_folder)
        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.result_folder))  # No files should be created

    def test_splitting_week_invalid_date_format(self):
        """Тест на неправильный формат даты."""
        invalid_date_data = "date;value\n2024-13-01;100\n"
        with open(self.test_file, 'w') as f:
            f.write(invalid_date_data)

        result = splitting_week(filename=self.test_file, result_folder=self.result_folder)
        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.result_folder))  # No files should be created

    def test_splitting_week_file_not_found(self):
        """Тест на случай отсутствия исходного файла."""
        result = splitting_week(filename=self.invalid_file, result_folder=self.result_folder)
        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.result_folder))  # No files should be created

    def test_result_folder_creation(self):
        """Тест на создание папки для результатов."""
        result = splitting_week(filename=self.test_file, result_folder=self.result_folder)
        self.assertTrue(os.path.exists(self.result_folder))

if __name__ == '__main__':
    unittest.main()
