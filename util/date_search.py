import pandas as pd

class DataFrameIterator:
    def __init__(self, dataframe: pd.DataFrame):
        """Инициализация итератора для строк датафрейма.
        
        Аргументы:
            dataframe: pandas DataFrame
        """
        self.dataframe = dataframe
        self.row_iterator = dataframe.iterrows()

    def __iter__(self):
        return self

    def __next__(self):
        """Получить следующую строку датафрейма.
        
        Возвращает:
            Следующую строку датафрейма.
        """
        return next(self.row_iterator)

def create_dataset_from_files(files: list):
    """Создать pandas DataFrame из списка файлов.
    
    Аргументы:
        files: список путей к файлам.
        
    Возвращает:
        pandas DataFrame, содержащий объединенные данные из файлов.
    """
    if len(files) == 1:
        # Если только один файл, просто читаем его в DataFrame
        return pd.read_csv(files[0], sep=";")
    
    elif len(files) >= 2:
        data_frames = []
        
        # Читаем все файлы в DataFrame
        for filename in files:
            data_frames.append(pd.read_csv(filename, sep=";"))
        
        # Если файлов два и хотя бы один из них имеет одну колонку, объединяем по колонкам
        if len(files) == 2 and (data_frames[0].shape[1] == 1 or data_frames[1].shape[1] == 1):
            if data_frames[0].shape[1] == 1:
                return pd.concat([data_frames[0], data_frames[1]], axis=1)
            else:
                return pd.concat([data_frames[1], data_frames[0]], axis=1)
        
        # Если файлов больше двух, объединяем их по строкам
        result_data_frame = pd.DataFrame()
        for data_frame in data_frames:
            result_data_frame = pd.concat([result_data_frame, data_frame], axis=0)
        
        return result_data_frame

def get_value(date: str, files: list):
    """Получить значение для указанной даты из списка файлов.
    
    Аргументы:
        date: строка с датой в формате yyyy-mm-dd.
        files: список путей к файлам.
        
    Возвращает:
        Значение для данной даты, если найдено, или None, если не найдено.
    """
    data_frame = create_dataset_from_files(files)
    
    # Итерируем по строкам DataFrame
    for index, line in DataFrameIterator(data_frame):
        if line.iloc[0] == date:
            return line.iloc[1]
    return None

def main():
    # Запрашиваем пути до файлов
    print("Введите пути до файлов (например, ./dataset.csv): ", end="")
    files = input().strip()
    if not files:
        files = "./dataset.csv"  # Если ввод пустой, используем дефолтный файл
    files = files.split(" ")  # Разделяем по пробелам, чтобы получить список файлов

    # Запрашиваем дату
    print("Введите дату (например, гггг-мм-дд): ", end="")
    date = input().strip() or "гггг-мм-дд"  # Если дата не введена, используем дефолтную

    # Получаем значение для указанной даты
    value = get_value(date=date, files=files)
    
    if value is not None:
        print(f"Значение для {date}: {value}")
    else:
        print(f"Значение для {date} не найдено.")

if __name__ == '__main__':
    main()
