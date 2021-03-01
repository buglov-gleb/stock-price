# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)

import re
import requests
import random

reDict = {'TSLA' : r'(\bт[еэ]сл.{1,2}\b|\bte?sla.{0,1}\b)', 'SBER.ME' : r'(\bсбер[ -]?банк.{0,2}\b|\bсбер.{0,2}\b)', 'GAZP.ME' : r'(\bгаз[ -]?пром.{0,2}\b|\bgaz[ -]?p.{0,3}\b)', 'LKOH.ME' : r'(\bлуко[йи]л.{0,2}\b|\blukoil.{0,2}\b|\blkoh\b)', 'VTBR.ME' : r'(\bвтб.{0,2}\b|\bvtb.{0,2}\b)', 'ROSN.ME' : r'(\bроснефт.{0,2}\b)', 'GMKN.ME' : r'(\bнор.*[ -]?никел.{1,3}\b|\bgmkn\b)', 'CHMF.ME' : r'(\bсеверстал.{0,2}\b|\bchmf\b)', 'YNDX.ME' : r'(\bяндекс.{0,2}\b|\by[a]?nd[e]?x\b)', 'SNGSP.ME' : r'(\bсургут[ -]?нефте[ -]?газ.{0,2}\b)', 'MGNT.ME' : r'(\bмагнит.{0,2}\b|\bm[a]?gn[i]?t\b)'}


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        },
        "session_state": {
            "city": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': get_random_stock(user_id)
        }

        res['response']['text'] = 'Привет! Подскажи, цену какой акции ты хочешь посмотреть?'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    for i in reDict:
        if re.search(reDict[i], req['request']['original_utterance'], re.IGNORECASE):
            api_result = requests.get('https://query1.finance.yahoo.com/v10/finance/quoteSummary/' + i + '?modules=price')
            if api_result:
                api_response = json.loads(api_result.content.decode('utf-8'))
                regularMarketPrice = api_response['quoteSummary']['result'][0]['price']['regularMarketPrice']['fmt']
                currency = api_response['quoteSummary']['result'][0]['price']['currency']

                res['response']['text'] = 'Сейчас стоимость акций ' + i +  " " + regularMarketPrice + " " + currency + "."
                res['response']['buttons'] = [{'title': "Подробнее", 'hide': True}]
                res['session_state']['city'] = i
            else:
                res['response']['text'] = 'С сервером неполадочка... Вернусь в скором времени!'
            return

    if req['request']['original_utterance'].lower() in [
        'помощь',
        'что ты умеешь',
        'что вы умеете'
    ]:
        sessionStorage[user_id] = {
            'suggests': get_random_stock(user_id)
        }
        res['response']['text'] = 'Я умею всего-ничего, подсказывать стоимость акций!'
        res['response']['buttons'] = get_suggests(user_id)
        #res['session_state']['city'] = req['state']['session']['city']
        return

    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'Все говорят "%s", а ты купи GameStop!' % (
        req['request']['original_utterance']
    )
    #res['session_state']['city'] = req['state']['session']['city']

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][2:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
#    if len(suggests) < 2:
#        suggests.append({
#            "title": "Холодновато!",
#            "url": "https://thenorthface.com",
#            "hide": True
#        })

    return suggests

def get_random_stock(user_id):
    randomStocks = random.sample(list(reDict.keys()), 2)
    return randomStocks
