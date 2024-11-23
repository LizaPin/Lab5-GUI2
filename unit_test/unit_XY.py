import unittest
import tempfile
import os
import sys
# Добавляем путь к корневой директории проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.splitting_x_y import splitting_x_y

class TestSplittingXY(unittest.TestCase):

    def setUp(self):
        # Создаем временный файл с тестовыми данными
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dataset_path = os.path.join(self.temp_dir.name, "dataset.csv")
        self.x_file_path = os.path.join(self.temp_dir.name, "splitXY", "x.csv")
        self.y_file_path = os.path.join(self.temp_dir.name, "splitXY", "y.csv")

        # Данные для тестов
        self.valid_data = "date;value\n2024-01-01;100.5\n2024-01-02;200.0\n2024-01-03;300.75\n"
        self.invalid_data = "date;value\n2024-01-01;100.5\n2024-01-02\ninvalid_line\n"

        # Создаем временный файл с валидными данными
        with open(self.dataset_path, "w") as f:
            f.write(self.valid_data)

    def tearDown(self):
        # Удаляем временные файлы и папки
        self.temp_dir.cleanup()

    def test_splitting_x_y_success(self):
        # Позитивный сценарий: корректный входной файл
        result = splitting_x_y(filename=self.dataset_path, x_file=self.x_file_path, y_file=self.y_file_path)
        self.assertTrue(result)

        # Проверяем, что файлы созданы и содержат ожидаемые данные
        self.assertTrue(os.path.exists(self.x_file_path))
        self.assertTrue(os.path.exists(self.y_file_path))

        with open(self.x_file_path, "r") as x_file, open(self.y_file_path, "r") as y_file:
            x_data = x_file.read().strip().split("\n")
            y_data = y_file.read().strip().split("\n")

        self.assertEqual(x_data, ["2024-01-01", "2024-01-02", "2024-01-03"])
        self.assertEqual(y_data, ["100.5", "200.0", "300.75"])

    def test_splitting_x_y_invalid_format(self):
        # Негативный сценарий: файл с неверным форматом данных
        with open(self.dataset_path, "w") as f:
            f.write(self.invalid_data)

        result = splitting_x_y(filename=self.dataset_path, x_file=self.x_file_path, y_file=self.y_file_path)
        self.assertFalse(result)

        # Проверяем, что файлы не созданы
        self.assertFalse(os.path.exists(self.x_file_path))
        self.assertFalse(os.path.exists(self.y_file_path))

    def test_splitting_x_y_file_not_found(self):
        # Исключительная ситуация: исходный файл не найден
        nonexistent_path = os.path.join(self.temp_dir.name, "nonexistent.csv")
        result = splitting_x_y(filename=nonexistent_path, x_file=self.x_file_path, y_file=self.y_file_path)
        self.assertFalse(result)

        # Проверяем, что файлы не созданы
        self.assertFalse(os.path.exists(self.x_file_path))
        self.assertFalse(os.path.exists(self.y_file_path))

    def test_splitting_x_y_directory_creation(self):
        # Проверяем создание директорий для выходных файлов
        result = splitting_x_y(filename=self.dataset_path, x_file=self.x_file_path, y_file=self.y_file_path)
        self.assertTrue(result)

        # Проверяем, что директория была создана
        self.assertTrue(os.path.exists(os.path.dirname(self.x_file_path)))
        self.assertTrue(os.path.exists(os.path.dirname(self.y_file_path)))

if __name__ == "__main__":
    unittest.main()
