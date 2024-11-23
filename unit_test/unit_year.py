import unittest
import tempfile
import os
import sys
# Добавляем путь к корневой директории проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.splitting_year import splitting_year

class TestSplittingYear(unittest.TestCase):

    def setUp(self):
        # Создаем временный каталог для тестовых файлов
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dataset_path = os.path.join(self.temp_dir.name, "dataset.csv")
        self.result_folder = os.path.join(self.temp_dir.name, "splitByYear")

        # Пример валидных данных
        self.valid_data = (
            "date;value\n"
            "2024-01-01;100.5\n"
            "2024-02-01;200.0\n"
            "2023-12-31;300.75\n"
            "2023-11-01;150.25\n"
        )
        
        # Пример данных с ошибками
        self.invalid_data = (
            "date;value\n"
            "invalid_line\n"
            "2024-01-01;100.5\n"
            "wrong_format;200.0\n"
        )

    def tearDown(self):
        # Удаляем временные файлы и папки
        self.temp_dir.cleanup()

    def test_splitting_year_success(self):
        # Позитивный сценарий: корректный входной файл
        with open(self.dataset_path, "w") as f:
            f.write(self.valid_data)
        
        result = splitting_year(filename=self.dataset_path, result_folder=self.result_folder)
        self.assertTrue(result)

        # Проверяем, что файлы созданы по годам
        year_2023_file = os.path.join(self.result_folder, "2023.csv")
        year_2024_file = os.path.join(self.result_folder, "2024.csv")

        self.assertTrue(os.path.exists(year_2023_file))
        self.assertTrue(os.path.exists(year_2024_file))

        # Проверяем содержимое файла за 2023 год
        with open(year_2023_file, "r") as f:
            data = f.read().strip()
        self.assertEqual(data, "2023-12-31;300.75\n2023-11-01;150.25")

        # Проверяем содержимое файла за 2024 год
        with open(year_2024_file, "r") as f:
            data = f.read().strip()
        self.assertEqual(data, "2024-01-01;100.5\n2024-02-01;200.0")

    def test_splitting_year_invalid_format(self):
        # Негативный сценарий: файл с неверным форматом данных
        with open(self.dataset_path, "w") as f:
            f.write(self.invalid_data)
        
        result = splitting_year(filename=self.dataset_path, result_folder=self.result_folder)
        self.assertTrue(result)

        # Проверяем, что созданы только файлы с валидными строками
        year_2024_file = os.path.join(self.result_folder, "2024.csv")
        self.assertTrue(os.path.exists(year_2024_file))

        with open(year_2024_file, "r") as f:
            data = f.read().strip()
        self.assertEqual(data, "2024-01-01;100.5")


    def test_splitting_year_directory_creation(self):
        # Проверяем создание папки для результатов
        with open(self.dataset_path, "w") as f:
            f.write(self.valid_data)
        
        result = splitting_year(filename=self.dataset_path, result_folder=self.result_folder)
        self.assertTrue(result)

        # Убедимся, что папка была создана
        self.assertTrue(os.path.exists(self.result_folder))

if __name__ == "__main__":
    unittest.main()
