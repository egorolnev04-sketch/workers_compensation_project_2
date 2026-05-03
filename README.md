# Проект: Прогнозирование стоимости страховых выплат

## Описание проекта
Разработана модель машинного обучения для предсказания итоговой стоимости страхового возмещения (UltimateIncurredClaimCost) на основе характеристик работника и параметров страхового случая.

## Датасет
- **Источник:** OpenML (ID: 42876)
- **Название:** Workers Compensation
- **Количество записей:** 100 000
- **Количество признаков:** 14
- **Целевая переменная:** UltimateIncurredClaimCost

## Используемые модели
- Linear Regression
- Ridge Regression
- Random Forest
- XGBoost

## Метрики качества
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² Score

## Лучшая модель
Random Forest показала лучшие результаты:
- R² ≈ 0.85
- MAE < $2000

## Структура проекта
workers_compensation_project/

│
├── app.py                  # Главный файл (навигация)

├── analysis_and_model.py   # Анализ данных и обучение модели

├── presentation.py         # Страница с презентацией

├── requirements.txt        # Зависимости

├── README.md               # Описание проекта

│

├── video/

│   └── demo.mp4            # Видео-демонстрация


## Установка и запуск
1. Установите зависимости:
   pip install -r requirements.txt

2. Запустите приложение:
   streamlit run app.py

## Функционал приложения
1. Загрузка данных из OpenML
2. Обучение 4 моделей регрессии
3. Сравнение метрик (MAE, RMSE, R²)
4. График важности признаков
5. Интерактивная форма для прогнозирования (14 полей)
6. Презентация проекта

## Ключевые признаки
- InitialCaseEstimate (начальная оценка)
- Age (возраст)
- WeeklyPay (зарплата)
- Gender, MaritalStatus
- DependentChildren, DependentsOther
- HoursWorkedPerWeek, DaysWorkedPerWeek, PartTimeFullTime
- ClaimDescription (тип травмы)
- ReportingDelay (задержка отчёта)
- AccidentMonth, AccidentDayOfWeek

## Видео-демонстрация
Файл video/demo.mp4 содержит запись работы приложения.

## Автор
Ольнев Егор Андреевич
# Проект: Прогнозирование стоимости страховых выплат

## Описание проекта
Разработана модель машинного обучения для предсказания итоговой стоимости страхового возмещения (UltimateIncurredClaimCost) на основе характеристик работника и параметров страхового случая.

## Датасет
- **Источник:** OpenML (ID: 42876)
- **Название:** Workers Compensation
- **Количество записей:** 100 000
- **Количество признаков:** 14
- **Целевая переменная:** UltimateIncurredClaimCost

## Используемые модели
- Linear Regression
- Ridge Regression
- Random Forest
- XGBoost

## Метрики качества
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² Score

## Лучшая модель
Random Forest показала лучшие результаты:
- R² ≈ 0.85
- MAE < $2000

## Структура проекта
workers_compensation_project/
│
├── app.py                  # Главный файл (навигация)
├── analysis_and_model.py   # Анализ данных и обучение модели
├── presentation.py         # Страница с презентацией
├── requirements.txt        # Зависимости
├── README.md               # Описание проекта
│
├── video/
│   └── demo.mp4            # Видео-демонстрация
│
└── data/
    └── workers_compensation.csv

## Установка и запуск
1. Установите зависимости:
   pip install -r requirements.txt

2. Запустите приложение:
   streamlit run app.py

## Функционал приложения
1. Загрузка данных из OpenML
2. Обучение 4 моделей регрессии
3. Сравнение метрик (MAE, RMSE, R²)
4. График важности признаков
5. Интерактивная форма для прогнозирования (14 полей)
6. Презентация проекта

## Ключевые признаки
- InitialCaseEstimate (начальная оценка)
- Age (возраст)
- WeeklyPay (зарплата)
- Gender, MaritalStatus
- DependentChildren, DependentsOther
- HoursWorkedPerWeek, DaysWorkedPerWeek, PartTimeFullTime
- ClaimDescription (тип травмы)
- ReportingDelay (задержка отчёта)
- AccidentMonth, AccidentDayOfWeek

## Видео-демонстрация
Файл video/demo.mp4 содержит запись работы приложения.

## Автор
Ольнев Егор Андреевич

## Дата
Май 2026
