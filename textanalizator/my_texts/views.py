from django.utils import timezone
from django.shortcuts import render
from .models import Articles
from .forms import ArticleForms
from .main_logic import logic, generate_plot
from .cont_parcing import Content_parcing
from .cont_parcing import get_cont
from .ml_logic import general_analiz_interface
from datetime import datetime






def my_texts_home(request):
    if request.method == 'GET':
        query = request.GET.get('db_query')
        sources = request.GET.get('sources')
        date = request.GET.get('date')



        if sources!= "all":
            if sources == "news":
                sources = 'Новости'
            elif sources == "banks":
                sources = "Банки ру"

            if query:
                if date:# проверяем, что запрос не пустой

                    try:
                        date = datetime.strptime(date, '%Y-%m-%d').date()
                        text = Articles.objects.filter(source = sources,query=query, date__contains=date)
                    except Articles.DoesNotExist:
                        # Обработка случая, если не найдено ни одного элемента с заданной тональностью
                        text = 'Такого источника не существует!'
                    except Exception as e:
                        # Обработка других исключений
                        text = f"Что-то пошло не так...\n{e}"

                    return render(request, 'my_texts/texts.html', {'text': text})
                else:
                    try:
                        # Получить все элементы с определенной тональностью
                        text = Articles.objects.filter(source=sources, query=query)
                    except Articles.DoesNotExist:
                        # Обработка случая, если не найдено ни одного элемента с заданной тональностью
                        text = 'Такого источника не существует!'
                    except Exception as e:
                        # Обработка других исключений
                        text = f"Что-то пошло не так...\n{e}"

                    return render(request, 'my_texts/texts.html', {'text': text})

            else:
                if date:
                    date = datetime.strptime(date, '%Y-%m-%d').date()
                    text = Articles.objects.filter(source = sources ,date__contains=date)
                    return render(request, 'my_texts/texts.html', {'text': text})
                else:
                    text = Articles.objects.filter(source=sources)
                    return render(request, 'my_texts/texts.html', {'text': text})
        else:
            if query:
                if date:# проверяем, что запрос не пустой

                    try:
                        date = datetime.strptime(date, '%Y-%m-%d').date()

                        text = Articles.objects.filter(query=query, date__contains = date)
                    except Articles.DoesNotExist:
                        # Обработка случая, если не найдено ни одного элемента с заданной тональностью
                        text = 'Такого источника не существует!'
                    except Exception as e:
                        # Обработка других исключений
                        text = f"Что-то пошло не так...\n{e}"

                    return render(request, 'my_texts/texts.html', {'text': text})
                else:
                    try:
                        # Получить все элементы с определенной тональностью
                        text = Articles.objects.filter(query=query)
                    except Articles.DoesNotExist:
                        # Обработка случая, если не найдено ни одного элемента с заданной тональностью
                        text = 'Такого источника не существует!'
                    except Exception as e:
                        # Обработка других исключений
                        text = f"Что-то пошло не так...\n{e}"

                    return render(request, 'my_texts/texts.html', {'text': text})
            if date:
                try:
                    date = datetime.strptime(date, '%Y-%m-%d').date()
                    text = Articles.objects.filter(date__contains =date)
                except Articles.DoesNotExist:
                    # Обработка случая, если не найдено ни одного элемента с заданной тональностью
                    text = 'Такого источника не существует!'
                except Exception as e:
                    # Обработка других исключений
                    text = f"Что-то пошло не так...\n{e}"

                return render(request, 'my_texts/texts.html', {'text': text})





            else:
                # В случае пустого запроса можно выполнить какие-то дополнительные действия или вернуть ошибку
                text = Articles.objects.all()
                return render(request, 'my_texts/texts.html', {'text': text})

    text = Articles.objects.all()
    return render(request, 'my_texts/texts.html', {'text': text})

def create(requests):
    tone = 'None'
    if requests.method == 'POST':
        form = ArticleForms(requests.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.source = 'client'
            analiz = general_analiz_interface(requests.POST['content'])
            article.tone = analiz
            article.date = timezone.now()
            article.save()

            tone = analiz

            data = {
                'form': form,
                'tone': tone
            }

            return render(requests, 'my_texts/create.html', data)



    form = ArticleForms()

    data = {
        'form': form
    }

    return render(requests, 'my_texts/create.html', data)
def find(request):



    return render(request, 'my_texts/find.html')
def cont_(request):
    if request.method == 'GET':
        db_query = request.GET.get('db_query')
        query = request.GET.get('query')
        source = request.GET.get('source')
        sources = request.GET.get('sources')# получаем значение поля запроса из GET-параметра
        if db_query:
            if sources!= "all":

                if sources == "news":
                    sources = 'Новости'
                elif sources == "banks":
                    sources = "Банки"
                try:
                    # Получить все элементы с определенной тональностью
                    text = Articles.objects.filter(source = sources, query=db_query)
                except Articles.DoesNotExist:
                    # Обработка случая, если не найдено ни одного элемента с заданной тональностью
                    text = 'Такого источника не существует!'
                except Exception as e:
                    # Обработка других исключений
                    text = f"Что-то пошло не так...\n{e}"
            else:
                try:
                    # Получить все элементы с определенной тональностью
                    text = Articles.objects.filter(query=db_query)
                except Articles.DoesNotExist:
                    # Обработка случая, если не найдено ни одного элемента с заданной тональностью
                    text = 'Такого источника не существует!'
                except Exception as e:
                    # Обработка других исключений
                    text = f"Что-то пошло не так...\n{e}"
            return render(request, 'my_texts/texts.html', {'text': text})
        if sources:
            if sources == "news":
                sources = 'Новости'
            elif sources == "banks":
                sources = "Банки"
            try:
                if sources == "all":
                    text = Articles.objects.all()
                # Получить все элементы с определенной тональностью
                else:
                    text = Articles.objects.filter(source=sources)
            except Articles.DoesNotExist:
                # Обработка случая, если не найдено ни одного элемента с заданной тональностью
                text = 'Такого источника не существует!'
            except Exception as e:
                # Обработка других исключений
                text = f"Что-то пошло не так...\n{e}"
            return render(request, 'my_texts/texts.html', {'text': text})
         # В случае пустого запроса можно выполнить какие-то дополнительные действия или вернуть ошибку

        if query:  # проверяем, что запрос не пустой
            if source == 'data_base':
                try:
                    # Получить все элементы с определенной тональностью
                    text = Articles.objects.filter(source=query)
                except Articles.DoesNotExist:
                    # Обработка случая, если не найдено ни одного элемента с заданной тональностью
                    text = 'Такого источника не существует!'
                except Exception as e:
                    # Обработка других исключений
                    text = f"Что-то пошло не так...\n{e}"
                return render(request, 'my_texts/texts.html', {'text': text})

            elif source =='news':
                text = Content_parcing.url_parciing(f'https://ria.ru/search/?query={query}',query)
                return render(request, 'my_texts/content.html', {'text': text})

            else:
                text = get_cont(query)
                for item in text:
                    article, created = Articles.objects.get_or_create(text_id=item['comment_id'], defaults={
                        'source': "Банки ру",  # Предполагая, что source должен быть равен значению из data
                        'content': item['text'],
                        'tone': item['tone'],
                        'query': item['name']
                    })
                    #article = Articles(
                    #    source="Банки",  # Предполагая, что source должен быть равен запросу (URL)
                    #    content=i['text'],
                    #    tone=i['tone'],
                    #
                    #)
                    article.save()

                return render(request, 'my_texts/banki.html', {'text': text})
                # передаем данные в шаблон
        else:
            if source == 'data_base':


                text = Articles.objects.all()
                return render(request, 'my_texts/texts.html', {'text': text})
            elif source == 'news':
                text = Content_parcing.url_parciing(f'https://ria.ru/search/?query=')
                return render(request, 'my_texts/content.html', {'text': text})

            else:
                text = get_cont()

                for item in text:

                    article, created = Articles.objects.get_or_create(text_id=item['comment_id'], defaults={
                        'source': "Банки ру", # Предполагая, что source должен быть равен значению из data
                        'content': item['text'],
                        'tone': item['tone'],
                        'query': item['name']
                    })
                    article.save()


                return render(request, 'my_texts/banki.html', {'text': text})
def get_some_content(request):


    if request.method == 'GET':
        url = request.GET.get('url')
        query = request.GET.get('query')  # Получаем URL из GET-параметра
        if url:
            # Выполняем ваш метод, который парсит содержимое страницы по полученному URL
            # Например, можно использовать Content_parcing.logic(url)
            text = Content_parcing.content_parcing(url)

            article = Articles(
                source="Новости",
                content=text['text_part'],
                tone=text['ton'],
                query=query
            )

            # Сохраняем экземпляр в базу данных
            article.save()

            # Здесь должен быть спарсенный текст
            # Здесь можно выполнить какие-то обработки текста перед выводом

            return render(request, 'my_texts/some_content.html', {'text': text})  ## Возвращаем спарсенный текст в HTTP-ответе
        else:
            pass
def dynamic_analysis(request):
    if request.method == 'GET':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        query = request.GET.get('db_query')


        if start_date_str and end_date_str and query:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

                # Ищем статьи с датами в заданном диапазоне
                articles = Articles.objects.filter(query = query,date__range=[start_date, end_date])
                res = logic(articles)

                return render(request, 'my_texts/dynamic_analysis.html', {'res': res})
            except ValueError:
                # Обработка некорректного формата дат или других ошибок
                return render(request, 'error.html', {'message': 'Некорректный формат даты'})
        elif start_date_str and query:
            try:
                today = datetime.now().date()
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.combine(today, datetime.max.time())

                # Ищем статьи с датами в заданном диапазоне
                articles = Articles.objects.filter(query=query, date__range=[start_date, end_date])
                res = logic(articles)

                return render(request, 'my_texts/dynamic_analysis.html', {'res': res})
            except ValueError:
                # Обработка некорректного формата дат или других ошибок
                return render(request, 'error.html', {'message': 'Некорректный формат даты'})
        elif end_date_str and query:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                # Ищем статьи с датами в заданном диапазоне
                articles = Articles.objects.filter(query=query, date__contains=end_date)
                res = logic(articles)

                return render(request, 'my_texts/dynamic_analysis.html', {'res': res})
            except ValueError:
                # Обработка некорректного формата дат или других ошибок
                return render(request, 'error.html', {'message': 'Некорректный формат даты'})
        elif start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                # Ищем статьи с датами в заданном диапазоне
                articles = Articles.objects.filter(date__range=[start_date, end_date])
                res = logic(articles)

                return render(request, 'my_texts/dynamic_analysis.html', {'res': res})
            except ValueError:
                # Обработка некорректного формата дат или других ошибок
                return render(request, 'error.html', {'message': 'Некорректный формат даты'})
        if end_date_str:
            try:

                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                # Ищем статьи с датами в заданном диапазоне
                articles = Articles.objects.filter(date__contains= end_date)

                res = logic(articles)

                return render(request, 'my_texts/dynamic_analysis.html', {'res': res})
            except ValueError:
                # Обработка некорректного формата дат или других ошибок
                return render(request, 'error.html', {'message': 'Некорректный формат даты'})
        if start_date_str:
            try:
                today = datetime.now().date()
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.combine(today, datetime.max.time())
                # Ищем статьи с датами в заданном диапазоне
                articles = Articles.objects.filter(date__range=[start_date, end_date])
                datetime.combine(today, datetime.max.time())
                res = logic(articles)
                plot_div = generate_plot(res)

                return render(request, 'my_texts/dynamic_analysis.html', {'res': res, 'plot_div': plot_div, })
            except ValueError:
                # Обработка некорректного формата дат или других ошибок
                return render(request, 'error.html', {'message': 'Некорректный формат даты'})





    return render(request, 'my_texts/dynamic_analysis.html')