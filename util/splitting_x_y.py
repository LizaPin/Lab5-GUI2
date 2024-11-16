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
        # Создаем папку splitXY, если она не существует
        os.makedirs(os.path.dirname(x_file), exist_ok=True)
        os.makedirs(os.path.dirname(y_file), exist_ok=True)
        
        # Открываем исходный файл и файлы для записи
        with open(filename, "r") as file, open(x_file, "w") as dates_file, open(y_file, "w") as values_file:
            # Пропускаем заголовок, если он есть
            header = file.readline().strip()
            if header.lower().startswith(("дата", "date")):
                print("Обнаружен заголовок, он будет пропущен.")
            
            for line in file:
                # Разделяем строку на дату и цену
                date_and_value = line.strip().split(';')
                
                if len(date_and_value) != 2:
                    # Если строка не состоит из двух элементов, выводим предупреждение
                    print(f"Неподходящий формат строки: {line.strip()}. Строка пропущена.")
                    continue
                
                # Записываем дату в файл x и цену в файл y
                dates_file.write(date_and_value[0] + "\n")
                values_file.write(date_and_value[1] + "\n")
        
        return True
    
    except Exception as e:
        # Ловим любые ошибки при открытии/чтении/записи файлов
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
