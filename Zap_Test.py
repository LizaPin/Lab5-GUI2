import os
import subprocess

def execute_scripts_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".py"):  # Проверяем только Python-скрипты
            file_path = os.path.join(folder_path, file_name)
            print(f"Выполняется файл: {file_name}")
            subprocess.run(["python", file_path], check=True)

if __name__ == "__main__":
    folder = "./unit_test"  # Укажите путь к папке
    execute_scripts_in_folder(folder)
