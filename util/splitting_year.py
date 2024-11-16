import re
import os

def splitting_year(filename="./dataset.csv", result_folder="./splitByYear"):
    """Разделить датасет по годам, создавая несколько CSV файлов.

    Аргументы:
        filename (str): Путь до исходного файла с данными.
        result_folder (str): Путь до папки для сохранения результатов.
    
    Возвращает:
        bool: True, если успешно, иначе False.
    """
    try:
        # Создаем папку по умолчанию, если она не указана
        os.makedirs(result_folder, exist_ok=True)

        with open(filename, "r") as file:
            # Пропускаем строку с заголовками (если есть)
            header = file.readline().strip()
            if header.lower().startswith(("дата", "date")):
                print("Обнаружен заголовок, он будет пропущен.")

            dates = []  # Список для хранения дат
            values = []  # Список для хранения значений
            current_year = ""  # Текущий год, с которым мы работаем
            
            for line in file:
                # Разделяем строку на дату и значение
                date_and_value = line.strip().split(';')
                
                # Пытаемся извлечь год из даты с помощью регулярного выражения
                match = re.match(r"(\d{4})-\d{2}-\d{2}", date_and_value[0])
                if match:
                    year = match.group(1)  # Извлекаем год
                else:
                    print(f"Неправильный формат строки: {line.strip()}. Пропущено.")
                    continue

                # Если год изменился, сохраняем старые данные в файл и очищаем списки
                if current_year != year:
                    if current_year:
                        save_to_csv(dates, values, result_folder, current_year)  # Сохраняем данные за предыдущий год
                    current_year = year  # Обновляем текущий год
                    dates.clear()  # Очищаем список дат
                    values.clear()  # Очищаем список значений

                # Добавляем текущую дату и значение в списки
                dates.append(date_and_value[0])
                values.append(date_and_value[1])

            # Сохраняем данные за последний год
            if dates:
                save_to_csv(dates, values, result_folder, current_year)

        return True
    except Exception as e:
        print(f"Ошибка: {e.__class__.__name__} - {str(e)}")
        return False


def save_to_csv(dates, values, result_folder, year):
    """Сохраняет данные в CSV файл по году."""
    try:
        # Создаем имя файла на основе года
        result_file_name = f"{result_folder}/{year}.csv"
        
        # Открываем файл для записи
        with open(result_file_name, mode="w") as result_file:
            for date, value in zip(dates, values):
                result_file.write(f"{date};{value}\n")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e.__class__.__name__} - {str(e)}")


def main():
    # Запрашиваем путь до исходного файла
    filename = input("Введите путь до файла (по умолчанию: ./dataset.csv): ").strip() or "./dataset.csv"
    
    # Запрашиваем путь до папки для сохранения результатов
    result_folder = input("Введите путь до папки для сохранения результатов (по умолчанию: ./splitByYear): ").strip() or "./splitByYear"
    
    # Вызываем функцию splitting_year и выводим результат
    if splitting_year(filename=filename, result_folder=result_folder):
        print("Успех")
    else:
        print("Провал")


if __name__ == '__main__':
    main()
