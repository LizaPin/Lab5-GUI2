# Работа с курсом корейской вонны

Это приложение на **PyQt5** для анализа и обработки данных из CSV-файлов. Оно позволяет выполнять такие действия, как разделение данных по неделям или годам, построение графиков и фильтрацию данных.

## Особенности

- Загрузка и отображение данных из CSV-файлов.
- Разделение данных:
  - По годам.
  - По неделям.
  - На `X` и `Y` для дальнейшего анализа.
  - Поиск значения курса на определенный день
- Построение графиков:
  - За весь период.
  - По определённому периоду.
  - За определённый месяц.
- Фильтрация данных по отклонению.
- Создание аннотаций к данным.


## Запуск
Нажмите на Dobrota_Trojan, оно все сделает за вас 🥴


## Использование

### Загрузка данных

1. Перейдите в меню **Файл → Открыть** и выберите CSV-файл.
2. Данные автоматически загрузятся в таблицу.

### Обработка данных

На вкладке **Обработка данных** доступны функции:
- **Получить данные**: поиск значения по конкретной дате.
- **Разделить на X и Y**: сохранение данных в отдельные файлы.
- **Разделить по годам**: создание отдельных файлов для каждого года.
- **Разделить по неделям**: создание отдельных файлов для каждой недели.

### Анализ данных

На вкладке **Анализ данных** доступны функции:
- **Фильтр по отклонению**: фильтрация данных по заданному значению отклонения.
- Построение графиков:
  - **За весь период**.
  - **По определённому периоду**.
  - **За месяц**.

### Создание аннотаций

Перейдите в меню **Файл → Создать аннотацию**, чтобы создать аннотацию для текущего набора данных.

## Структура кода

- **`MainWindow`**: основной класс приложения.
- **`initUI`**: инициализация пользовательского интерфейса.
- **Обработка вкладок**:
  - **`init_processing_tab`**: вкладка для обработки данных.
  - **`init_analysis_tab`**: вкладка для анализа данных.
- **Функции обработки**: `splitting_x_y`, `splitting_years`, `splitting_weeks`.
- **Функции анализа**: `filter_data`, `show_full_graph`, `show_period_graph`, `show_month_graph`.

## Зависимости

- **PyQt5**: для интерфейса.
- **Pandas**: для работы с данными.
- **Matplotlib**: для построения графиков.

## Цветовая палитра интерфейса

- Основной цвет интерфейса: **#DDA0DD** (сиреневый).
- Цвет меню: **#8A2BE2** (фиолетовый).
- Цвет текста: чёрный/белый для контраста.

