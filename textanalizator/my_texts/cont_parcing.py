import requests
from bs4 import BeautifulSoup
import lxml
import time
from .ml_logic import general_analiz_interface
import asyncio


def getSearchApiUrl():
    return "https://www.banki.ru/services/responses/list/ajax/";


def getSearchApiParameters(page=1, commentType=None, rates=None, product=None, bank=None):
    return {
        'is_countable': 'on',
        'product': product,
        'type': commentType,
        'page': page,
        'rate[]': rates,
        'bank': bank
    }


def getSearchApiHeaders():
    return {
        'accept': 'application/json',
        'accept-language': 'ru-RU,ru;q=0.9',
        'content-type': 'application/json',
        'referer': 'https://www.banki.ru/services/responses/list/product/deposits/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }


def getSearchApiCookies():
    return {

    }


def SendRequest(page, commentType=None, rates=None, product=None, bank=None):
    url = getSearchApiUrl()
    params = getSearchApiParameters(page, commentType, rates, product, bank)
    headers = getSearchApiHeaders()
    cookies = getSearchApiCookies()

    response = requests.get(url, params=params, cookies=cookies, headers=headers)
    return response.json()


def GetAllComments(commentType=None, rates=None, product=None, bank=None):
    resultList = []
    counter = 0
    flag = True
    while flag:
        counter += 1
        currentRequestResult = SendRequest(counter, commentType, rates, product, bank)
        resultList = resultList + currentRequestResult['data']
        flag = currentRequestResult['hasMorePages']
        yield currentRequestResult
    return resultList


def getting_filtered_data(SendRequest, query):
    data = SendRequest(1)['data']
    filtered_data = []
    if query:
        for i in range(len(data)):
            if query == data[i]['company']['url']:
                filtered_data.append(
                    {
                        'comment_id': data[i]['id'],
                        'title': data[i]['title'],
                        'text': data[i]['text'].replace('<p>', '').replace('</p>', '').replace('\r',
                                                                                                                   '').replace(
                    '\n', '').replace('\xa0', ''),
                        'name': data[i]['company']['name'],
                        'code': data[i]['company']['url'],
                        'tone': general_analiz_interface(data[i]['text'].replace('<p>', '').replace('</p>', '').replace('\r',
                                                                                                                   '').replace(
                    '\n', '').replace('\xa0', '')),
                        'source': "https://www.banki.ru/services/responses/list/ajax/"
                    }
                )
    else:
        for i in range(len(data)):
            filtered_data.append(
                {
                    'comment_id': data[i]['id'],
                    'title': data[i]['title'],
                    'text': data[i]['text'].replace('<p>', '').replace('</p>', '').replace('\r',
                                                                                           '').replace(
                        '\n', '').replace('\xa0', ''),
                    'name': data[i]['company']['name'],
                    'code': data[i]['company']['url'],
                    'tone': general_analiz_interface(
                        data[i]['text'].replace('<p>', '').replace('</p>', '').replace('\r',
                                                                                       '').replace(
                            '\n', '').replace('\xa0', '')),
                    'source': "https://www.banki.ru/services/responses/list/ajax/"
                }
            )
    return filtered_data

def get_cont(query=None):
    return getting_filtered_data(SendRequest,query)

class Content_parcing():





    @staticmethod
    def url_parciing(url, query=None):

        ff = []

        responce = requests.get(url)
        soup = BeautifulSoup(responce.text, "lxml")
        body = soup.find('div', class_="list")
        title = body.find_all(class_="list-item__title color-font-hover-only")

        img_tag = body.find_all('img')
        img_url = []
        for i in range(len(img_tag)):
            if img_tag[i]:
                img_url.append(img_tag[i]['src'])

        for i in range(len(title)):
            texts = {

                'title': str(title[i].text),
                'url': str(title[i].get('href')),
                'img_url': str(img_url[i]),
                'query': query
            }
            ff.append(texts)

        return (ff)

    @staticmethod
    def content_parcing(url):
        temp = ''
        responce = requests.get(url)
        soup = BeautifulSoup(responce.text, "lxml")
        body = soup.find('div', class_="article__body")
        content = body.find_all(class_=lambda x: x and 'text' in x)
        for i in range(len(content)):
            temp += f' {(content[i].text)}'


        full_content = {
            "text_part": temp,
            "ton": general_analiz_interface(temp)
        }

        return full_content