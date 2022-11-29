import argparse
import logging

import redis
import requests
import hashlib
import json
import datetime
from sanic import Sanic, response
# from handle_bulk_data import red_customers
from bot_responses import generate_response

logger = logging.getLogger(__name__)

DEFAULT_SERVER_PORT = 7114

DEFAULT_SANIC_WORKERS = 1

REDIS_HOST = "20.122.155.51"
REDIS_PORT = 6379
REDIS_DB = 11
REDIS_DB_1=15
REDIS_PASSWORD = "sam@1234"
REDIS_DB_CONV = "0"
red = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD,charset="utf-8", decode_responses=True)
red_customers = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_1, password=REDIS_PASSWORD,charset="utf-8", decode_responses=True)
def maintain_time_log(start_time,end_time,session_id):
    # try:
    delay=end_time-start_time
    with open("time_tracker.txt","a") as f:
        f.write("session_id %s"%session_id+"\t"+"Incoming Time %s"%start_time+"\t"+"Response Time %s"%end_time+"\t"+"Delay %s"%delay+"\n")
    # except IOError:
    #     with open("time_tracker.txt","w+") as f:
    #         f.write("Incoming Time %s"%start_time+"\t"+"Response Time %s"%end_time+"\n")
    return
def in_time_log(start_time,session_id):
    print("******************")
    print("Session id:",session_id)
    print("Start time:",start_time)
    with open("in_time_tracker.txt","a") as f:
        f.write("session_id %s"%session_id+"\t"+"Incoming Time %s"%start_time+"\n")


def create_argument_parser():
    """Parse all the command line arguments for the nlg server script."""

    parser = argparse.ArgumentParser(description="starts the nlg endpoint")
    parser.add_argument(
        "-p",
        "--port",
        default=DEFAULT_SERVER_PORT,
        type=int,
        help="port to run the server at",
    )
    parser.add_argument(
        "--workers",
        default=DEFAULT_SANIC_WORKERS,
        type=int,
        help="Number of processes to spin up",
    )

    return parser

mapped_languages={
    "english":"en",
    "hindi":"hi",
    "tamil":"tam",
    "telugu":"tel",
    "kannada":"ka",
    "malayalam":"ml",
    "marathi":"ma",
    "punjabi":"pa",
    "bangla":"bn",
    "gujarati":"gu"
}
def detect_language_from_redis(data):
    user_id=data['user_id']
    data=red_customers.hgetall(user_id)
    print("data",data)
    lang = data.get("language").lower()
    return mapped_languages[lang]

def detect_language(data):
    print("data",data)
    user_id=data['user_id']
    print("phone_number",user_id)
    with open("customer_details.json", "r+") as f:
        customer_details = json.load(f)
    for customer in customer_details:
        if customer['phone_number']==int(user_id):
            return customer["custom_field_2"]
    user_id="12345"
    for customer in customer_details:
        if int(customer['phone_number'])==user_id:
            return customer["custom_field_2"]
    return "en"


def run_server(port, workers):
    app = Sanic(__name__)

    @app.route("/webhook", methods=["POST", "OPTIONS"])
    async def nlg(request):
        """Endpoint which processes the Core request for a bot response."""
        print("entering herer------------?")
        nlg_call = request.json
        print(nlg_call)
        nlu_data = nlg_call.get("nlu_data", None)
        sender_id = nlg_call.get("sender",None)
        print("sender_id",sender_id)
        print("nlu_data",nlu_data)
        if nlu_data is None:
            print("Inside the nlu_data is None:",nlu_data)
            red.hset("cz",sender_id,"yes")
            red.hset("backend",sender_id,"no")
        else:
            red.hset("cz",sender_id,"no")
            red.hset("backend",sender_id,"yes")
        data=red.hget("cz",sender_id)
        print("data",data)
        if data == "yes":
            print("inside yes")
            language=detect_language(nlg_call)
        else:
            print("inside no")
            language=detect_language_from_redis(nlg_call)
        print("Language:",language)
        try:
            nlg_call = request.json
            in_time=datetime.datetime.now()
            print("NLG data:",nlg_call)
            in_time_log(in_time,nlg_call["sender"])
            print("language>>>>>>>",language)
            data = {
                "english":"en",
                "tamil":"tam",
                "telugu":"tel",
                "kannada":"ka",
                "bengali":"bn",
                "malayalam":"ml",
                "hindi":"hi",
                "marathi":"ma",
                "punjabi":"pa",
                "gujarati":"gu"
            }
            ASR_Language_code  = {
                "english":"en-IN",
                "tamil":"ta-IN",
                "telugu":"te-IN",
                "kannada":"kn-IN",
                "bengali":"bn-IN",
                "malayalam":"ml-IN",
                "hindi":"hi-IN",
                "marathi":"mr-IN",
                "punjabi":"pa-Guru-IN"
            }
            # in_time=datetime.datetime.now()
            print("NLG data:",nlg_call)
            # in_time_log(in_time,nlg_call["sender"])
            if language.lower()=="en":
                bot_response = await generate_response(nlg_call)
            elif language.lower()=="hi":
                bot_response=requests.post("http://localhost:7115/webhook/",json=nlg_call).json()
            elif language.lower()=="tam":
                bot_response=requests.post("https://srirambot.saarthi.ai/sriram_tamil/webhook/",json=nlg_call).json()
            elif language.lower()=="tel":
                bot_response=requests.post("http://localhost:7117/webhook/",json=nlg_call).json()
            elif language.lower() == "ka":
                print("language-------->",language)
                bot_response=requests.post("http://localhost:7566/webhook/",json=nlg_call).json()
            elif language.lower() == "bn":
                bot_response=requests.post("https://srirambot.saarthi.ai/sriram_bangla/webhook/",json=nlg_call).json()
            elif language.lower() == "ml":
                bot_response=requests.post("https://srirambot.saarthi.ai/sriram_malayalam/webhook/",json=nlg_call).json()
            elif language.lower() == "ma":
                bot_response = requests.post("https://srirambot.saarthi.ai/sriram_marathi/webhook/",json = nlg_call).json()
            elif language.lower() == "pa":
                bot_response = requests.post("https://srirambot.saarthi.ai/sriram_punjabi/webhook/",json = nlg_call).json()
            elif language.lower() == "gu":
                bot_response = requests.post("https://srirambot.saarthi.ai/sriram_gujarati/webhook/",json = nlg_call).json()
            # end_time=datetime.datetime.now()
            # maintain_time_log(in_time,end_time,nlg_call['sender'])
            return response.json(bot_response)
        except:
            logging.error("Error Message")
    app.run(host="0.0.0.0", port=port, workers=workers)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Running as standalone python application
    arg_parser = create_argument_parser()
    cmdline_args = arg_parser.parse_args()

    run_server(cmdline_args.port, cmdline_args.workers)
