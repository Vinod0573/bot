import asyncio
import logging
from datetime import datetime
from calendar import monthrange
import re
from dateutil import relativedelta
from aiohttp import ClientSession, ClientConnectorError
from flask import Flask, request, jsonify

# from googletrans import Translator

logger = logging.getLogger(__name__)

# translator = Translator(
#     service_urls=[
#       'translate.google.co.in', 
#       'translate.google.com']
#     )

import requests
import datetime

URLS = [
    'http://20.84.16.150:80/api/v1/service/production-bfsi-nlu/score',
]

hindi_to_english = {
    "नेक्सट": "अगला",
    "दिस": "यह",
    "फर्स्ट": "प्रथम",
    "सैकंड": "दूसरा",
    "लास्ट": "पिछले",
    "बिफोर": "पहले",
    "प्रीवियस": "पिछला",
    "मंडे": "सोमवार",
    "ट्यूसडे": "मंगलवार",
    "वेडनेसडे": "बुधवार",
    "थर्सडे": "गुरूवार",
    "फ्राइडे": "शुक्रवार",
    "सैटरडे": "शनिवार",
    "संडे": "रविवार",
    "जनुअरी": "जनवरी",
    "फेब्रुअरी": "फ़रवरी",
    "मार्च": "जुलूस",
    "अप्रैल": "अप्रैल",
    "मई": "मई",
    "जून": "जून",
    "जुलाई": "जुलाई",
    "अगस्त": "अगस्त",
    "सितम्बर": "सितंबर",
    "अक्टूबर": "अक्टूबर",
    "नवंबर": "नवंबर",
    "दिसंबर": "दिसंबर"
}

other_dates = {
    "दिन": "day",
    "दिनों": "days",
    "हफ्ता": "week",
    "हफ्ते": "weeks",
    "सप्ताह": "week",
    "अगले": "next",
    "डे": "day"
}
app = Flask(__name__)
loop = asyncio.new_event_loop()


def handle_other_dates(message):
    day_flag = False
    week_flag = False
    numeric_value = None
    if "दिन" in message or "दिनों" in message or "डे" in message:
        day_flag = True
    if "हफ्ता" in message or "हफ्ते" in message or "सप्ताह" in message:
        week_flag = True
    for item in message:
        if item.isdigit():
            numeric_value = item
            break
    if numeric_value and day_flag:
        return get_duckling_entities("call me after {} {}".format(numeric_value, "days"))
    if week_flag:
        return get_duckling_entities("call me next week")
    if day_flag and numeric_value is None:
        return get_duckling_entities("call me in a day")


async def fetch_html(url: str, session: ClientSession, **kwargs):
    msg = kwargs['msg']
    try:
        resp = await session.request(method="POST", url=url, json={"data": str(msg)})
    except ClientConnectorError:
        return (url, 404)
    return await resp.json()


async def make_requests(urls, **kwargs) -> None:
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                fetch_html(url=url, session=session, **kwargs)
            )
        results = await asyncio.gather(*tasks)

    return results


def extract_date_time(duckling_response):
    entity = {}
    if duckling_response:
        try:
            if duckling_response[0]['dim'] == 'time':

                if 'value' in duckling_response[0]['value']:
                    str_date_time = duckling_response[0]['value']['value']
                    date_time_obj = datetime.datetime.strptime(str_date_time[:16], '%Y-%m-%dT%H:%M')
                    user_time_diff = datetime.datetime.strptime(str_date_time[:19], '%Y-%m-%dT%H:%M:%S')
                    curr_time = datetime.datetime.now()
                    print(curr_time, user_time_diff)
                    time_diff = (curr_time - user_time_diff).total_seconds()
                    print("TIME DIFF: ", time_diff)
                    if time_diff <= 5 and time_diff >= -10:
                        return entity
                    else:
                        entity['time'] = date_time_obj.strftime('%I %M %p')
                        entity['date'] = date_time_obj.strftime('%d/%m/%Y')
                        entity['start'] = duckling_response[0]['start']
                        entity['end'] = duckling_response[0]['end']
                    return entity

                elif 'values' in duckling_response[0]['value']:
                    print("IN VALUES")
                    str_date_time = duckling_response[0]['value']['from']['value']
                    print("STR: ", str_date_time)
                    date_time_obj = datetime.datetime.strptime(str_date_time[:16], '%Y-%m-%dT%H:%M')
                    user_time_diff = datetime.datetime.strptime(str_date_time[:19], '%Y-%m-%dT%H:%M:%S')
                    curr_time = datetime.datetime.now()
                    print(curr_time, user_time_diff)
                    time_diff = (curr_time - user_time_diff).total_seconds()
                    print("TIME DIFF: ", time_diff)
                    if time_diff <= 5 and time_diff >= -10:
                        return entity
                    else:
                        entity['time'] = date_time_obj.strftime('%I %M %p')
                        entity['date'] = date_time_obj.strftime('%d/%m/%Y')
                        entity['start'] = duckling_response[0]['start']
                        entity['end'] = duckling_response[0]['end']
                    return entity
                else:
                    return entity


        except:
            return entity
    else:
        return entity

def get_date(message):
    match=re.search(r"[0-9]+",message)
    entity_details=[]
    if match:
        given_number=int(match.group(0))
        print("Given number:",given_number)
        if given_number>0:
            current_day=datetime.datetime.now().day
            current_month=datetime.datetime.now().month
            current_year=datetime.datetime.now().year
            predict_month=current_month
            predict_year=current_year
            if given_number<current_day:
                if current_month==12:
                    predict_month=1
                    predict_year=current_year+1
                else:
                    predict_month=current_month+1
                num_days=monthrange(predict_year,predict_month)
                if len(str(predict_month))==1:
                    predict_month="0"+str(predict_month)
                if given_number<=num_days[1]:
                    entity_details.append({
                        'confidence': 1.0,
                        'end': match.span()[1],
                        'entity': 'date',
                        'extractor': 'bot_date',
                        'start': match.span()[0],
                        'value': str(given_number)+"/"+str(predict_month)+"/"+str(predict_year)[2:]
                    })
                else:
                    entity_details.append({
                        'confidence': 1.0,
                        'end': match.span()[1],
                        'entity': 'number',
                        'extractor': 'bot_number',
                        'start': match.span()[0],
                        'value': str(given_number)
                    })
            else:
                num_days=monthrange(predict_year,predict_month)
                if len(str(predict_month))==1:
                    predict_month="0"+str(predict_month)
                if given_number<=num_days[1]:
                    entity_details.append({
                        'confidence': 1.0,
                        'end': match.span()[1],
                        'entity': 'date',
                        'extractor': 'bot_date',
                        'start': match.span()[0],
                        'value': str(given_number)+"/"+str(predict_month)+"/"+str(predict_year)[2:]
                    })
                else:
                    entity_details.append({
                        'confidence': 1.0,
                        'end': match.span()[1],
                        'entity': 'number',
                        'extractor': 'bot_number',
                        'start': match.span()[0],
                        'value': str(given_number)
                    })
        else:
            entity_details.append({
                'confidence': 1.0,
                'end': match.span()[1],
                'entity': 'number',
                'extractor': 'bot_number',
                'start': match.span()[0],
                'value': str(given_number)
            })
    if "नेक्स्ट मंथ" in message or "अगले महीने" in message:
        next_month=datetime.date.today()+relativedelta.relativedelta(months=1)
        date=str(next_month.day)+"/"+str(next_month.month)+"/"+str(next_month.year)[2:]
        entity_details.append({
                'confidence': 1.0,
                'end': len(message),
                'entity': 'date',
                'extractor': 'bot_date',
                'start': 0,
                'value': date
            })
    return entity_details
def get_duckling_entities(message):
    try:
        data = [('locale', 'en_IN'), ('text', message), ('tz', 'localtime')]
        duckling_response = requests.post('http://168.62.57.226/duckling', data=data).json()

        print("DUCKLING UNFORMATTED: ", duckling_response)

        time_date_entity = extract_date_time(duckling_response)
        duckling_entity = []

        if time_date_entity:

            if time_date_entity['date']:
                duckling_entity.append({
                    "confidence": 1.0,
                    "end": time_date_entity['end'],
                    "entity": "date",
                    "extractor": "duckling",
                    "start": time_date_entity['start'],
                    "value": time_date_entity['date']
                })

            if time_date_entity['time'] and time_date_entity['time'] != '12 00 AM':
                duckling_entity.append({
                    "confidence": 1.0,
                    "end": time_date_entity['end'],
                    "entity": "time",
                    "extractor": "duckling",
                    "start": time_date_entity['start'],
                    "value": time_date_entity['time']
                })
        return duckling_entity, duckling_response
    except:
        return []


def replace_english_words_in_english_utterance(text):
    for item in hindi_to_english:
        if item in text:
            text.replace(item, hindi_to_english[item])

    return text


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/model/parse', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    data = request.json

    msg = data["text"]
    print(msg)

    nlu = dict()
    if str(msg).lower() == "hello" or str(msg).lower() == "hey":
        nlu['intent'] = {'name': 'greet', 'confidence': 1.0}
        nlu['entities'] = []
        nlu['intent_ranking'] = [{'name': 'greet', 'confidence': 1.0},
                                 {'name': 'affirm', 'confidence': 0.00000003},
                                 {'name': 'deny', 'confidence': 0.0000000001}]
        nlu['text'] = str(msg)
    else:
        # intent_response = requests.post('http://52.170.156.208//emi_english_nlu/module/predict', json = {"text": str(msg)}).json()
        # print(intent_response)
        intent_response = loop.run_until_complete(make_requests(urls=URLS, msg=msg))
        print("intent_response", intent_response)
        formatted_intent_response = []
        for item in intent_response[0]["label"]:
            formatted_intent_response.append({"name": item["name"], "confidence": float(item["confidence"])})
        # intent_response = requests.post('http://localhost:9135/model/parse', json={"text": str(msg)}).json()

        print("intent_response", intent_response)
        msg = replace_english_words_in_english_utterance(str(msg))
        try:
            entity_response = requests.post('http://52.147.223.178:80/api/v1/service/production-ner/score',json={"data": str(msg),"lang":"english"}).json()
        except:
            logging.error("English NER link error")
            entity_response={"entities":[]}
        print("The entity response is *************",entity_response)
        # entity_response={"entities":[]}
        for item in entity_response["entities"]:
            if item["entity"] == "time" and "DF" in item["value"]:
                value = item["value"].replace("DF", "").replace(" 00", "")
                value = "call me after {} hours".format(value)
                duckling_response, _duckling_response = get_duckling_entities(value)
                for entity in duckling_response:
                    if entity["entity"] == "time":
                        item["value"] = entity["value"]
                    date_flag = False
                    if entity["entity"] == "date":
                        for date_entity in entity_response["entities"]:
                            if date_entity["entity"] == "date":
                                date_flag = True
                        if not date_flag:
                            entity_response["entities"].append(entity)
        print("entity response", entity_response)
        # print("Duckling response", duckling_response)

        nlu['intent'] = formatted_intent_response[0]
        nlu['intent_ranking'] = formatted_intent_response
        nlu['text'] = msg

        entities = []
        date_value = None
        time_value = None

        # if "entities" in entity_response and len(entity_response["entities"]) == 0:
        #     entity_response["entities"] = handle_other_dates(msg)
        if "entities" in entity_response and len(entity_response["entities"]) == 0:
            entity_response['entities']= get_date(msg)

        if entity_response and 'entities' in entity_response and entity_response["entities"] is not None:
            for entity in entity_response['entities']:
                if date_value is None and entity["entity"] == "date":
                    try:
                        formatted_date = datetime.datetime.strptime(entity["value"], "%d/%m/%Y")
                    except ValueError:
                        formatted_date = datetime.datetime.strptime(entity["value"], "%d/%m/%y")
                    date_value = formatted_date.strftime("%d/%m/%y")
                    entity["value"] = formatted_date.strftime("%d/%m/%y")
                    entities.append(entity)
                if time_value is None and entity["entity"] == "time":
                    time_value = entity["value"]
                    entities.append(entity)

        nlu['entities'] = entities
        message = data["text"]

        def isint(text):
            try:
                value = int(text)
                return True
            except:
                return False

        entity = dict()

        for item in message.split(" "):
            print(item)
            if "₹" in item:
                item = item.replace("₹", "")
            if isint(item):
                entity['entity'] = 'number'
                entity['value'] = str(item)
                entity['start'] = message.index(item)
                entity['end'] = message.index(item) + len(item)

        if entity:
            nlu["entities"].append(entity)

        print(nlu)
    return jsonify(nlu)


if __name__ == '__main__':
    app.run(debug=True, port=12214)
