import argparse
import logging

import redis
import requests
import hashlib

from sanic import Sanic, response

from bot_responses import generate_response_hindi

logger = logging.getLogger(__name__)

DEFAULT_SERVER_PORT = 7115

DEFAULT_SANIC_WORKERS = 1

REDIS_HOST = "20.122.155.51"
REDIS_PORT = 6379
REDIS_DB = 2
REDIS_PASSWORD = "sam@1234"
REDIS_DB_CONV = "0"
red = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, charset="utf-8",password=REDIS_PASSWORD)


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


def run_server(port, workers):
    app = Sanic(__name__)

    @app.route("/webhook", methods=["POST", "OPTIONS"])
    async def nlg(request):
        """Endpoint which processes the Core request for a bot response."""
        nlg_call = request.json
        bot_response = await generate_response_hindi(nlg_call)
        # print (bot_response)

        return response.json(bot_response)

    app.run(host="0.0.0.0", port=port, workers=workers)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Running as standalone python application
    arg_parser = create_argument_parser()
    cmdline_args = arg_parser.parse_args()

    run_server(cmdline_args.port, cmdline_args.workers)
