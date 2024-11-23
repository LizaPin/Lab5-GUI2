import os

def splitting_x_y(filename="./dataset.csv", x_file="./splitXY/x.csv", y_file="./splitXY/y.csv"):
    """Создать два CSV файла: x с датами и y с ценами из исходного датасета.

    Аргументы:
        filename (str): Путь до исходного файла с данными.
        x_file (str): Путь до файла для сохранения дат.
        y_file (str): Путь до файла для сохранения цен.
    
    Возвращает:
        bool: True, если успешно, иначе False.
    """
    try:
        # Проверяем существование исходного файла
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл {filename} не найден.")

        # Создаем папку splitXY, если она не существует
        os.makedirs(os.path.dirname(x_file), exist_ok=True)
        os.makedirs(os.path.dirname(y_file), exist_ok=True)

        # Открываем исходный файл
        with open(filename, "r") as file:
            # Пропускаем заголовок, если он есть
            header = file.readline().strip()
            if header.lower().startswith(("дата", "date")):
                print("Обнаружен заголовок, он будет пропущен.")

            # Создаем временные списки для дат и значений
            dates = []
            values = []

            for line in file:
                # Разделяем строку на дату и цену
                date_and_value = line.strip().split(';')

                if len(date_and_value) != 2:
                    # Если строка не состоит из двух элементов, выводим предупреждение
                    print(f"Неподходящий формат строки: {line.strip()}.")
                    return False  # Завершаем функцию

                # Добавляем данные во временные списки
                dates.append(date_and_value[0])
                values.append(date_and_value[1])

        # Записываем данные из временных списков в файлы
        with open(x_file, "w") as dates_file:
            dates_file.write("\n".join(dates))
        with open(y_file, "w") as values_file:
            values_file.write("\n".join(values))

        return True

    except FileNotFoundError as fnf_error:
        print(fnf_error)
        return False
    except Exception as e:
        # Ловим любые другие ошибки
        print(f"Ошибка: {e.__class__.__name__} - {str(e)}")
        return False


def main():
    # Запрашиваем путь до исходного файла
    filename = input("Введите путь до файла (по умолчанию: ./dataset.csv): ").strip() or "./dataset.csv"
    
    # Запрашиваем путь до файла для дат
    x_file = input("Введите путь для сохранения результатов  с датами (по умолчанию: ./splitXY/x.csv): ").strip() or "./splitXY/x.csv"
    
    # Запрашиваем путь до файла для цен
    y_file = input("Введите путь  для сохранения результатов c ценами (по умолчанию: ./splitXY/y.csv): ").strip() or "./splitXY/y.csv"
    
    # Вызываем функцию splitting_x_y и выводим результат
    if splitting_x_y(filename=filename, x_file=x_file, y_file=y_file):
        print("Успех")
    else:
        print("Провал")


if __name__ == '__main__':
    main()
