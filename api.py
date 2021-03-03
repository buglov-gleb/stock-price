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

reDict = {'TSLA' : r'(\bт[еэ]сл.{1,2}\b|\bte?sla.{0,1}\b)', 'SBER.ME' : r'(\bсбер[ -]?банк.{0,2}\b|\bсбер.{0,2}\b|\bSBER.*\b)', 'GAZP.ME' : r'(\bгаз[ -]?пром.{0,2}\b|\bgaz[ -]?p.{0,3}\b)', 'LKOH.ME' : r'(\bлуко[йи]л.{0,2}\b|\blukoil.{0,2}\b|\blkoh\b|\blkoh\.me\b)', 'VTBR.ME' : r'(\bвтб.{0,2}\b|\bvtb.{0,2}\b|\bVTBR\.ME\b)', 'ROSN.ME' : r'(\bроснефт.{0,2}\b|\brosn.*\b|\bROSN\.ME\b)', 'GMKN.ME' : r'(\bнор.*[ -]?никел.{1,3}\b|\bgmkn\b|\bGMKN\.ME\b)', 'CHMF.ME' : r'(\bсеверстал.{0,2}\b|\bchmf\b|\bCHMF\.ME\b)', 'YNDX.ME' : r'(\bяндекс.{0,2}\b|\by[a]?nd[e]?x\b|\bYNDX\.ME\b)', 'SNGSP.ME' : r'(\bсургут[ -]?нефте[ -]?газ.{0,2}\b|\bSNGSP\.ME\b)', 'MGNT.ME' : r'(\bмагнит.{0,2}\b|\bm[a]?gn[i]?t\b|\bMGNT\.ME\b)', 'TATN.ME' : r'(\bтат[ -]?нефт.{0,2}\b|\btatn.*\b|\bTATN\.ME\b)', 'TRNFP.ME' : r'(\bтранс[ -]?нефт.{0,2}\b|\btrnfp\b|\btrans[ -]?neft\b|\bTRNFP\.ME\b)', 'OZON.ME' : r'(\bозон.{0,2}\b|\bozon.{0,2}\b|\bOZON\.ME\b)', 'TCSG.ME' : r'(\bтинько.{1,3}\b|\btinkoff.{0,2}\b|\bTCS[g]\b|\bTCSG\.me\b)', 'MAIL.ME' : r'(\bмэ[ий]л.{0,2}\b|\bmail[\.]?.{0,2}\b|\bMAIL\.ME\b)', 'AAPL' : r'(\bэп[п]?л.{0,2}\b|\bap[p]?le\b|\bяблок.{1,2}\b\bAAPL\b)', 'AMZN' : r'(\bамазон.{0,2}\b|\bamazo.{1,2}\b|\bAMZN\b)', 'ALRS.ME' : r'(\bALROS.{1,2}\b|\bалрос.{1,2}\b|\bALRS\.ME\b)', 'GME' : r'(\bgame[ -]?stop.{0,1}\b|\bгейм[ -]?стоп.{0,2}\b)', 'BAC' : r'(bank of america|бэнк оф Америк.{1,2}|\bБанк.{0,2} Америки\b|\bBAC\b)', 'NIO' : r'(\bnio.{0,1}\b|\bнио\b)', 'MSFT' : r'(\bMSFT\b|\bMicrosoft\b|\bмикро[ -]?софт\b|\bмайкро[ -]?софт\b)', 'FB' : r'(\bFB\b|\bfacebook\b|\bфб\b|\bф[еэ]йс[ -]?бук.{0,2}\b)', 'BABA' : r'(\bBABA\b|\bali[ -]baba\b|\bали[ -]?баба\b)', 'NVDA' : r'(\bnvid[i]?a\b|\b[э]?нвидиа\b)', 'NFLX' : r'(\bNFLX\b|\bnetflix.{0,2}\b|\bн[еэ]тфлик.{0,3}\b)', 'ZM' : r'(\bZoom.{0,2}\b|\bzm\b|\bзум.{0,2}\b)', 'MRNA' : r'(\bMRNA\b|\bmoderna\b|\bмодерн.{1,2}\b)', 'F' : r'(\bF\b|\bford.{0,2}\b|\bфорд.{0,2}\b)', 'PFE' : r'(\bPFE\b|\bPfizer.{0,2}\b|\bпфизер.{0,2}\b|\b[п]?файзер.{0,2}\b)'}


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
            "stock": False
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
                currency = api_response['quoteSummary']['result'][0]['price']['currencySymbol']
                companyName = api_response['quoteSummary']['result'][0]['price']['shortName']
                res['response']['text'] = 'Сейчас стоимость акций ' + companyName +  " " + regularMarketPrice + " " + currency
                res['response']['buttons'] = [{'title': "Рекомендации", 'hide': True}]
                res['session_state']['stock'] = i
            else:
                res['response']['text'] = 'С сервером неполадочка... Вернусь в скором времени!'
            return

    if req['state']['session']['stock'] and req['request']['original_utterance'].lower() in [
        'рекомендации', 'рекомендуешь', 'еще', 'ещё', 'больше', 'рекомендовать'
    ]:
        api_result = requests.get('https://query1.finance.yahoo.com/v10/finance/quoteSummary/' + req['state']['session']['stock'] + '?modules=recommendationTrend')
        if api_result:
            api_response = json.loads(api_result.content.decode('utf-8'))
            strongBuy = str(api_response['quoteSummary']['result'][0]['recommendationTrend']['trend'][0]['strongBuy'])
            buy = str(api_response['quoteSummary']['result'][0]['recommendationTrend']['trend'][0]['buy'])
            hold = str(api_response['quoteSummary']['result'][0]['recommendationTrend']['trend'][0]['hold'])
            sell = str(api_response['quoteSummary']['result'][0]['recommendationTrend']['trend'][0]['sell'])
            strongSell = str(api_response['quoteSummary']['result'][0]['recommendationTrend']['trend'][0]['strongSell'])

            res['response']['text'] = 'Рекомендации для акции ' + req['state']['session']['stock'].split('.')[1] + '\nАктивно покупать:' + strongBuy + '\nПокупать:' + buy + '\nДержать:' + hold + '\nПродавать:' + sell + '\nАктивно продавать:' + strongSell
        else:
            res['response']['text'] = 'С сервером неполадочка... Вернусь в скором времени!'
        res['session_state']['stock'] = req['state']['session']['stock']
        return

    if req['request']['original_utterance'].lower() in [
        'помощь',
        'что ты умеешь',
        'что вы умеете'
    ]:
        sessionStorage[user_id] = {
            'suggests': get_random_stock(user_id)
        }
        res['response']['text'] = 'Я могу подсказать вам стоимость акций, а также сообщить по ним текущие рекомендации'
        res['response']['buttons'] = get_suggests(user_id)
        res['session_state']['stock'] = req['state']['session']['stock']
        return

    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'Все говорят "%s", а ты купи GameStop!' % (
        req['request']['original_utterance']
    )
    res['session_state']['stock'] = req['state']['session']['stock']

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

    return suggests

def get_random_stock(user_id):
    randomStocks = random.sample(list(key.split('.')[0] for key in reDict.keys()), 2)
    return randomStocks
