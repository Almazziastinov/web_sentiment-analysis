def logic(articles):
    tones_by_date = {}

    for article in articles:
        article_date = article.date.strftime('%Y-%m-%d')  # Преобразуем дату в строку формата 'YYYY-MM-DD'

        if article_date not in tones_by_date:
            tones_by_date[article_date] = {'positive': 0, 'negative': 0}

        if article.tone == 'Negative':
            tones_by_date[article_date]['negative'] += 1
        else:
            tones_by_date[article_date]['positive'] += 1

    return tones_by_date

from django.shortcuts import render
import plotly.graph_objs as go

def generate_plot(tones_by_date):
    # Подготовим данные для графика
    dates = list(tones_by_date.keys())
    dates_short = [date[:10] for date in dates]  # Берем только первые 10 символов
    positives = [tones_by_date[date]['positive'] for date in dates]
    negatives = [tones_by_date[date]['negative'] for date in dates]

    # Создаем объекты для графика
    trace1 = go.Bar(x=dates_short, y=positives, name='Позитивные', marker=dict(color='green'),
                    offset=-0.5)  # Устанавливаем отрицательное смещение для первой гистограммы
    trace2 = go.Bar(x=dates_short, y=negatives, name='Негативные', marker=dict(color='red'),
                    offset=0.5)  # Устанавливаем положительное смещение для второй гистограммы

    # Формируем данные для графика
    data = [trace1, trace2]
    layout = go.Layout(barmode='group', title='Тональность по дате')

    return go.Figure(data=data, layout=layout).to_html(full_html=False)

