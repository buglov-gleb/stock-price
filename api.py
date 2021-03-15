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

reDict = {'TSLA' : r'(\bт[еэ]сл.{1,2}\b|\bte?sla.{0,1}\b)', 'SBER.ME' : r'(\bсбер[ -]?банк.{0,2}\b|\bсбер.{0,2}\b|\bSBER.*\b)', 'GAZP.ME' : r'(\bгаз[ -]?пром.{0,2}\b|\bgaz[ -]?p.{0,3}\b)', 'LKOH.ME' : r'(\bлуко[йи]л.{0,2}\b|\blukoil.{0,2}\b|\blkoh\b|\blkoh\.me\b)', 'VTBR.ME' : r'(\bвтб.{0,2}\b|\bvtb.{0,2}\b|\bVTBR\.ME\b)', 'ROSN.ME' : r'(\bроснефт.{0,2}\b|\brosn.*\b|\bROSN\.ME\b)', 'GMKN.ME' : r'(\bнор.*[ -]?никел.{1,3}\b|\bgmkn\b|\bGMKN\.ME\b)', 'CHMF.ME' : r'(\bсеверстал.{0,2}\b|\bchmf\b|\bCHMF\.ME\b)', 'YNDX.ME' : r'(\bяндекс.{0,2}\b|\by[a]?nd[e]?x\b|\bYNDX\.ME\b)', 'SNGSP.ME' : r'(\bсургут[ -]?нефте[ -]?газ.{0,2}\b|\bSNGSP\.ME\b)', 'MGNT.ME' : r'(\bмагнит.{0,2}\b|\bma?gni?t\b|\bMGNT\.ME\b)', 'TATN.ME' : r'(\bтат[ -]?нефт.{0,2}\b|\btatn.*\b|\bTATN\.ME\b)', 'TRNFP.ME' : r'(\bтранс[ -]?нефт.{0,2}\b|\btrnfp\b|\btrans[ -]?neft\b|\bTRNFP\.ME\b)', 'OZON.ME' : r'(\bозон.{0,2}\b|\bozon.{0,2}\b|\bOZON\.ME\b)', 'TCSG.ME' : r'(\bтинько.{1,3}\b|\btinkoff.{0,2}\b|\bTCS[g]\b|\bTCSG\.me\b)', 'MAIL.ME' : r'(\bмэ[ий]л.{0,2}\b|\bmail[\.]?.{0,2}\b|\bMAIL\.ME\b)', 'AAPL' : r'(\bэп[п]?л.{0,2}\b|\bap[p]?le\b|\bяблок.{1,2}\b\bAAPL\b)', 'AMZN' : r'(\bамазон.{0,2}\b|\bamazo.{1,2}\b|\bAMZN\b)', 'ALRS.ME' : r'(\bALROS.{1,2}\b|\bалрос.{1,2}\b|\bALRS\.ME\b|\bALRS\b)', 'GME' : r'(\bgame[ -]?stop.{0,1}\b|\bгейм[ -]?стоп.{0,2}\b|\bGME\b)', 'BAC' : r'(bank of america|бэнк оф Америк.{1,2}|\bБанк.{0,2} Америки\b|\bBAC\b)', 'NIO' : r'(\bnio.{0,1}\b|\bнио\b)', 'MSFT' : r'(\bMSFT\b|\bMicrosoft\b|\bмикро[ -]?софт\b|\bмайкро[ -]?софт\b)', 'FB' : r'(\bFB\b|\bfacebook\b|\bфб\b|\bф[еэ]йс[ -]?бук.{0,2}\b)', 'BABA' : r'(\bBABA\b|\bali[ -]baba\b|\bали[ -]?баб.{1,2}\b)', 'NVDA' : r'(\bnv[i]?d[i]?a\b|\bэ?нвидиа\b)', 'NFLX' : r'(\bNFLX\b|\bnetflix.{0,2}\b|\bн[еэ]тфлик.{0,3}\b)', 'ZM' : r'(\bZoom.{0,2}\b|\bzm\b|\bзум.{0,2}\b)', 'MRNA' : r'(\bMRNA\b|\bmoderna\b|\bмодерн.{1,2}\b)', 'F' : r'(\bF\b|\bford.{0,2}\b|\bфорд.{0,2}\b)', 'PFE' : r'(\bPFE\b|\bPfizer.{0,2}\b|\bпфизер.{0,2}\b|\b[п]?файзер.{0,2}\b)', 'PLTR' : r'(\bPLTR\b|\bpalantir.{0,2}\b|\bпалантир.{0,2}\b)', 'RKT' : r'(\bRKT\b|\brocket.{0,2}\b|\bрокет.{0,2}\b)', 'GM' : r'(\bGM\b|\bgeneral motor.{0,2}\b|\bдженерал мотор.{0,2}\b|\bгенерал мотор.{0,2}\b)', 'TRIP' : r'(\bTRIP\b|\bTrip[ -]?Advisor\b|\bтрип[ -]?[аэ]двизор.{0,2}\b)', 'GOOGL' : r'(\bGOOGL[e]?\b|\bгуг[о]?л.{0,2}\b|\bAlphabet.{0,2}\b|\bал[ь]?фабет\b|\bалфавит.{0,2}\b)', 'TMVWY' : r'(\bTMVWY\b|\bTeam[ -]?Viewer\b|\bтим[ -]?вью[в]?ер\b)', 'MOEX.ME' : r'(\bMOEX\b|\bMOEX\.ME\b|\bмос[ -]?бирж.{1,2}\b|\bмосковс.* бирж.{1,2}\b|\bбирж.{1,2} москв.{0,2}\b)', 'INTC' : r'(\bINTC\b|\bintel\b|\bинт[еэ]л.{0,2}\b)', 'HPQ' : r'(\bHP[Q]\b|Hewlett?[ -]?Packard|\bэйч[ -]?пи\b|\bХьюлетт?[ -]?Пакк?ард\b)', 'ADBE' : r'(\bADBE\b|\badobe.{0,1}\b|\b[аэ]доб.{0,2}\b)', 'V' : r'(\bV\b|\bvisa\b|\bвиз.{1,2}\b)', 'IBM' : r'(\bIBM\b|\bInternational Business Machines\b|\bай[ -]?би[ -]?э?м.{0,2}\b|\bибм\b)', 'ORCL' : r'(\bORCL\b|\boracle\b|\bор[аэ]кл.{0,2}\b)', 'CSCO' : r'(\bCi?SCO\b|\b[цс]иско.{0,1}\b)', 'PYPL' : r'(\bPYPL\b|\bpay[ -]?pal\b|\bп[еаэ]йп[еаэ]л.{0,2}\b)', 'MA' : r'(\bMA\b|\bMaster[ -]?card\b|\bмастер[ -]?кард.{0,2}\b)', 'FIXP.ME' : r'(\bFIXP\b|\bFIXP\.ME\b|\bFix[ -]?Price\b|\bфикс[ -]?прайс.{0,2}\b)', 'UBER' : r'(\bUBER\b|\b[ую]бер.{0,2}\b)', 'EBAY' : r'(\bEBAY\b|\b[иеэ]б[эе]й.{0,1}\b)', 'TWTR' : r'(\bTWTR\b|\btwit?ter\b|\bтвитт?ер.{0,2}\b)', 'PINS' : r'(\bPINS\b|\bpinterest\b|\bпинт[эе]р[эе]ст.{0,2}\b)', 'SELG.ME' : r'(\bSELG\b|\bSELG\.ME\b|\bseligdar\b|\bселигдар.{0,2}\b)', 'LNZL.ME' : r'(\bLNZL\b|\bLNZL\.ME\b|\blen[ -]?zoloto\b|\bлен[ -]?золот.{0,2}\b)', 'PIKK.ME' : r'(\bPIKK\.ME\b|\bpik.{0,1}\b|\bпик.{0,2}\b)', 'MVID.ME' : r'(\bMVID\b|\bMVID\.ME\b|\bм[ \-\.,]?видео\b)', 'DSKY.ME' : r'(\bDSKY\b|\bDSKY\.ME\b|\bдетск.{0,2} мир.{0,2}\b)', 'LNTA.ME' : r'(\bLNTA\b|\bLNTA.ME\b|\bлент.{1,2}\b)', 'MTSS.ME' : r'(\bMTSS.ME\b|\bMTSS?\b|\bмтс\b)', 'HYDR.ME' : r'(\bHYDR\b|\bHYDR.ME\b|\bрус[ -]?гидро\b)', 'MSNG.ME' : r'(\bMSNG.ME\b|\bMSNG\b|мос[ -]?энерго\b)', 'ETSY' : r'(\bETSY\b|\bэтси\b)', 'UPWK' : r'(\bUPWK\b|\bupwork\b|апворк.{0,2}\b)', 'PM' : r'(\bPM\b|\bPhil?lip Morr?is\b|\bфилл?ип.{0,2} мор?рис.{0,2}\b)', 'MVIS' : r'(\bMVIS\b|\bMicro[ -]?Vision\b|\bмикро[ -]?вижн\b)', 'HLT' : r'(\bHLT\b|\bhilton\b|\bхилтон.{0,2}\b)', 'TWLO' : r'(\bTWLO\b|\bTwilio\b|\bтвилио\b)', 'UPS' : r'(\bUPS\b|\bю[ -]?пи[ -]?эс\b|\bю [-] ?пи [-] ?эс\b)', 'RLLCF' : r'(\bRLLCF\b|\bRolls[ -]Royce\b|\bрол?лс [-] ройс\b|\bрол?лс[ -]ройс\b)', '005930.KS' : r'(\b005930\b|\b005930\.KS\b|\bсамсунг.{0,2}\b|\bsamsung\b)'}


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
                regularMarketPrice = str(api_response['quoteSummary']['result'][0]['price']['regularMarketPrice']['raw'])
                currency = api_response['quoteSummary']['result'][0]['price']['currencySymbol']
                companyName = api_response['quoteSummary']['result'][0]['price']['shortName']
                res['response']['text'] = 'Сейчас стоимость акций ' + companyName +  " " + regularMarketPrice + " " + currency
                res['response']['buttons'] = [{'title': "Рекомендации", 'hide': True}]
                res['session_state']['stock'] = i
            else:
                res['response']['text'] = 'С сервером неполадочка... Вернусь в скором времени!'
            return

    if req['state']['session']['stock'] and any(x in ['рекомендации', 'рекомендуешь', 'еще', 'ещё', 'больше', 'рекомендовать'] for x in req['request']['original_utterance'].lower().split(' ')):
        api_result = requests.get('https://query1.finance.yahoo.com/v10/finance/quoteSummary/' + req['state']['session']['stock'] + '?modules=recommendationTrend')
        if api_result:
            api_response = json.loads(api_result.content.decode('utf-8'))
            strongBuy = str(api_response['quoteSummary']['result'][0]['recommendationTrend']['trend'][1]['strongBuy'])
            buy = str(api_response['quoteSummary']['result'][0]['recommendationTrend']['trend'][1]['buy'])
            hold = str(api_response['quoteSummary']['result'][0]['recommendationTrend']['trend'][1]['hold'])
            sell = str(api_response['quoteSummary']['result'][0]['recommendationTrend']['trend'][1]['sell'])
            strongSell = str(api_response['quoteSummary']['result'][0]['recommendationTrend']['trend'][1]['strongSell'])

            res['response']['text'] = 'Рекомендации для акции ' + req['state']['session']['stock'].split('.')[0] + '\nАктивно покупать: ' + strongBuy + '\nПокупать: ' + buy + '\nДержать: ' + hold + '\nПродавать: ' + sell + '\nАктивно продавать: ' + strongSell
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
