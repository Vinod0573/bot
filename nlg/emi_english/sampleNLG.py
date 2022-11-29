import argparse
import logging
import requests
import ast

from sanic import Sanic, response

logger = logging.getLogger(__name__)

DEFAULT_SERVER_PORT = 13025

DEFAULT_SANIC_WORKERS = 1


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


async def generate_response(nlg_call):
    """Mock response generator.

    Generates the responses from the bot's domain file.
    """
    args = nlg_call.get("arguments", {})
    print("Args", args)
    template = nlg_call.get("template")
    bot_response = dict()

    import json
    utterance = 'English Utterance'
    with open("Navi_responses.json", "r+", encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        if item and "Utterance Name" in item and item["Utterance Name"] == template and \
                utterance in item:
            if "buttons" in item and item["buttons"] and item["buttons"] == "":
                text = "".join(x.get(utterance, '') for x in item)
                args_list = list(args.keys())
                if len(args_list) == 0:
                    bot_response["text"] = text
                else:
                    text = text.format(**args)
                    bot_response["text"] = text
            else:
                text = "".join(item.get(utterance))
                # text = response["response"]["response"][0].get('Response','')
                print("TEXT: ", text)
                args_list = list(args.keys())
                print("ARG: ", args_list)
                if len(args_list) == 0:
                    bot_response["text"] = text
                else:
                    text = text.format(**args)
                    bot_response["text"] = text

                x = ast.literal_eval(item["buttons"]) if "buttons" in item and \
                                                         item["buttons"] else []
                bot_response["buttons"] = x
    return bot_response

    # try:
    #     utterance = 'English Utterance'
    #     url = "http://13.92.118.170/sheetapi/navi/UtterResponse?utterTemplate={}".format(template)
    #     print("URL", url)
    #     import time
    #     start_time = time.time()
    #     response = requests.get(url).json()
    #     end_time = time.time()
    #     print("NLG response time :::::::::", (end_time - start_time))
    #     print(response)
    #     if response.get("status_code"):
    #         if response["status_code"] != 200:
    #             bot_response[
    #                 "text"] = "Response Sheet API is currently down. Kindly try chatting to bot after some time."
    #             return bot_response
    #
    #
    # except requests.exceptions.HTTPError as errh:
    #     logger.exception("Http Error: {}".format(errh))
    #     bot_response["text"] = "Response Sheet API is currently down. Kindly try chatting to bot after some time."
    #     return bot_response
    # except requests.exceptions.ConnectionError as errc:
    #     logger.exception("HError Connecting: {}".format(errc))
    #     bot_response["text"] = "Response Sheet API is currently down. Kindly try chatting to bot after some time."
    #     return bot_response
    # except requests.exceptions.Timeout as errt:
    #     logger.exception("Timeout Error: {}".format(errt))
    #     bot_response["text"] = "Response Sheet API is currently down. Kindly try chatting to bot after some time."
    #     return bot_response
    # except requests.exceptions.RequestException as err:
    #     logger.exception("Error: {}".format(err))
    #     bot_response["text"] = "Response Sheet API is currently down. Kindly try chatting to bot after some time."
    #     return bot_response
    #
    # utterance = 'English Utterance'
    # print("rresponse ", response)
    # if "buttons" in response["response"] and response["response"]["buttons"] and response["response"]["buttons"] == "":
    #     text = "".join(x.get(utterance, '') for x in response["response"]["response"])
    #     args_list = list(args.keys())
    #     if len(args_list) == 0:
    #         bot_response["text"] = text
    #     else:
    #         text = text.format(**args)
    #         bot_response["text"] = text
    # else:
    #     text = "".join(x.get(utterance, '') for x in response["response"]["response"])
    #     # text = response["response"]["response"][0].get('Response','')
    #     print("TEXT: ", text)
    #     args_list = list(args.keys())
    #     print("ARG: ", args_list)
    #     if len(args_list) == 0:
    #         bot_response["text"] = text
    #     else:
    #         text = text.format(**args)
    #         bot_response["text"] = text
    #
    #     x = ast.literal_eval(response["response"]["buttons"]) if "buttons" in response["response"] and \
    #                                                              response["response"]["buttons"] else []
    #     bot_response["buttons"] = x
    #
    # return bot_response


def run_server(port, workers):
    app = Sanic(__name__)

    @app.route("/nlg", methods=["POST", "OPTIONS"])
    async def nlg(request):
        """Endpoint which processes the Core request for a bot response."""
        nlg_call = request.json
        print("NLG Response", nlg_call)
        bot_response = await generate_response(nlg_call)

        return response.json(bot_response)

    app.run(host="0.0.0.0", port=port, workers=workers)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Running as standalone python application
    arg_parser = create_argument_parser()
    cmdline_args = arg_parser.parse_args()

    run_server(cmdline_args.port, cmdline_args.workers)
