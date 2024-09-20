import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Установка заголовка страницы
st.title('Диаграмма сгорания SYNERGY')

# Поля ввода
st.header('Параметры ввода')

# Общая работа
total_work = st.number_input(
    'Общая работа',
    min_value=0,
    value=100,
    step=1
)

# Оставшаяся работа
remaining_work_input = st.text_input(
    'Оставшаяся работа (значения через запятую)',
    '50,20,10,5,0'
)

# Преобразование входных данных в список чисел
try:
    remaining_work = [float(x.strip()) for x in remaining_work_input.split(',') if x.strip()]
except ValueError:
    st.error('Пожалуйста, введите числовые значения, разделенные запятыми, в поле "Оставшаяся работа".')
    st.stop()

# Дата начала
start_date = st.date_input('Дата начала', value=pd.to_datetime('2024-09-01'))

# Автоматическое определение количества периодов
periods = len(remaining_work) + 1  # Добавляем 1 для общей работы в начале

# Кнопка генерации
if st.button('Сгенерировать диаграмму сгорания'):
    # Генерация дат
    dates = pd.date_range(start=start_date, periods=periods)

    # Добавление общей работы в начало списка оставшейся работы
    actual_remaining_work = [total_work] + remaining_work

    # Проверка соответствия количества дат и оставшейся работы
    if len(dates) != len(actual_remaining_work):
        st.error('Количество значений оставшейся работы должно быть на единицу меньше количества периодов.')
    else:
        # Расчет идеальной оставшейся работы
        if len(dates) > 1:
            ideal_work = [
                total_work - (total_work / (len(dates) - 1)) * i
                for i in range(len(dates))
            ]
        else:
            ideal_work = [total_work]

        # Создание DataFrame с данными
        df = pd.DataFrame({
            'Дата': dates,
            'Реальная оставшаяся работа': actual_remaining_work,
            'Идеальная оставшаяся работа': ideal_work
        })

        # Преобразование DataFrame для Seaborn
        df_melted = df.melt('Дата', var_name='Тип работы', value_name='Оставшаяся работа')

        # Установка стиля
        sns.set(style="whitegrid")

        # Создание графика
        fig, ax = plt.subplots(figsize=(10, 6))

        # Построение реальной оставшейся работы
        sns.lineplot(
            data=df_melted[df_melted['Тип работы'] == 'Реальная оставшаяся работа'],
            x='Дата',
            y='Оставшаяся работа',
            label='Реальная оставшаяся работа',
            marker='o',
            linestyle='-',
            color='blue',
            ax=ax
        )

        # Построение идеальной оставшейся работы
        sns.lineplot(
            data=df_melted[df_melted['Тип работы'] == 'Идеальная оставшаяся работа'],
            x='Дата',
            y='Оставшаяся работа',
            label='Идеальная оставшаяся работа',
            marker='o',
            linestyle='--',
            color='red',
            ax=ax
        )

        # Форматирование дат на оси X
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
        ax.xaxis.set_major_locator(mdates.DayLocator())

        # Поворот меток дат для лучшей читаемости
        plt.xticks(rotation=45)

        # Установка заголовков и меток осей
        ax.set_title('Диаграмма сгорания SYNERGY')
        ax.set_xlabel('Дата')
        ax.set_ylabel('Оставшаяся работа')

        # Добавление сетки и легенды
        ax.grid(True)
        ax.legend()

        # Корректировка макета для предотвращения обрезки меток
        plt.tight_layout()

        # Отображение графика в Streamlit
        st.pyplot(fig)
