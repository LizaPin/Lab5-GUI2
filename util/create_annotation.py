import pandas as pd
import os

def create_annotation(filename: str, result_folder: str) -> bool:
    """
    Создаёт файл аннотации для заданного датасета.

    Аргументы:
        filename: Путь к файлу с датасетом.
        result_folder: Путь к папке, где будет сохранён файл аннотации.

    Возвращает:
        True, если аннотация успешно создана, иначе False.
    """
    try:
        # Чтение данных из файла CSV
        df = pd.read_csv(filename, sep=";")

        # Проверка существования папки для аннотации, если её нет — создаём
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)

        # Путь к файлу аннотации
        annotation_path = os.path.join(result_folder, "annotation.txt")

        # Запись аннотации в файл
        with open(annotation_path, "w", encoding="utf-8") as annotation_file:
            annotation_file.write(f"Путь до файла: {filename}\n")
            annotation_file.write(f"Количество строк: {len(df.index)}\n")
            annotation_file.write("Типы столбцов:\n")
            annotation_file.write(str(df.dtypes) + "\n")

        return True
    except Exception as e:
        print(f"Ошибка при создании аннотации: {e}")
        return False

def main():
    """Главная функция для взаимодействия с пользователем."""
    # Ввод пути до файла с датасетом
    filename = input("Введите путь до файла (./dataset.csv): ").strip()
    if not filename:
        filename = "./dataset.csv"
    
    # Ввод пути до папки для сохранения аннотации
    result_folder = input("Введите путь до папки, куда будет сохранён файл аннотации (./): ").strip()
    if not result_folder:
        result_folder = "./"

    # Попытка создать аннотацию
    if create_annotation(filename=filename, result_folder=result_folder):
        print("Аннотация успешно создана.")
    else:
        print("Произошла ошибка при создании аннотации.")

if __name__ == '__main__':
    main()
