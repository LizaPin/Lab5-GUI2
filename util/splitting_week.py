import os
import datetime

def splitting_week(filename="./dataset.csv", result_folder=""):
    """Разделить датасет по неделям и сохранить в несколько CSV файлов.

    Аргументы:
        filename (str): Путь до исходного файла с данными.
        result_folder (str): Путь до папки, куда будут сохранены результаты.
    
    Возвращает:
        bool: True, если успешно, иначе False.
    """
    try:
        # Убедимся, что папка для результатов существует или создадим её
        if result_folder:
            os.makedirs(result_folder, exist_ok=True)
        else:
            result_folder = "./"
        
        with open(filename, "r") as file:
            # Пропускаем строку с заголовками (если есть)
            header = file.readline().strip()
            
            dates = []  # Список для хранения дат
            values = []  # Список для хранения значений
            last_day_of_week = -1  # Индекс последнего дня недели

            for line in file:
                # Разделяем строку на дату и значение
                date_and_value = line.strip().split(';')
                
                if len(date_and_value) != 2:
                    # Проверяем, что строка состоит из двух элементов
                    print("Неправильный формат строки. Операция прервана.")
                    return False

                # Преобразуем строку с датой в объект datetime
                try:
                    date = datetime.datetime.strptime(date_and_value[0], "%Y-%m-%d")
                except ValueError:
                    print(f"Неправильный формат даты: {date_and_value[0]}. Операция прервана.")
                    return False

                current_day_of_week = date.weekday()  # Получаем день недели (0 - понедельник, 6 - воскресенье)
                
                # Сохраняем данные за предыдущую неделю, если день недели изменился
                if last_day_of_week < current_day_of_week and last_day_of_week != -1:
                    result_file_name = f"{result_folder}/{dates[0].replace('-', '')}_{dates[-1].replace('-', '')}.csv"
                    with open(result_file_name, mode="w") as result_file:
                        # Записываем данные в файл
                        for date_str, value in zip(dates, values):
                            result_file.write(f"{date_str};{value}\n")
                    
                    # Очищаем списки для новой недели
                    dates.clear()
                    values.clear()

                # Добавляем текущую дату и значение в списки
                dates.append(date_and_value[0])
                values.append(date_and_value[1])

                # Обновляем последний день недели
                last_day_of_week = current_day_of_week

        return True

    except Exception as e:
        # Обрабатываем исключения и выводим сообщение об ошибке
        print(f"Ошибка: {e.__class__.__name__} - {str(e)}")
        return False

def main():
    # Запрашиваем путь до входного файла
    filename = input("Введите путь до файла (по умолчанию: ./dataset.csv): ").strip() or "./dataset.csv"
    
    # Запрашиваем путь до папки для сохранения результатов
    result_folder = input("Введите путь до папки для сохранения результатов (по умолчанию: ./by_week): ").strip() or "./by_week"
    
    # Вызываем функцию splitting_week и выводим результат
    if splitting_week(filename=filename, result_folder=result_folder):
        print("Успех")
    else:
        print("Провал")


if __name__ == '__main__':
    main()


    