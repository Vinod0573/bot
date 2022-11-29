import asyncio
import inspect
import json
import logging
import uuid
from asyncio import Queue, CancelledError
from sanic import Sanic, Blueprint, response
from sanic.request import Request
from typing import Text, List, Dict, Any, Optional, Callable, Iterable, Awaitable
import hashlib

import rasa.utils.endpoints
from rasa.constants import DOCS_BASE_URL, DEFAULT_CUSTOM_MESSAGE
from rasa.core import utils

try:
    from urlparse import urljoin  # pytype: disable=import-error
except ImportError:
    from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class UserMessage(object):
    """Represents an incoming message.

     Includes the channel the responses should be sent to."""

    DEFAULT_SENDER_ID = "default"
    DEFAULT_REQUEST_ID = "default"
    DEFAULT_USER_ID = "default"

    def __init__(
        self,
        text: Optional[Text] = None,
        output_channel: Optional["OutputChannel"] = None,
        sender_id: Optional[Text] = None,
        request_id: Optional[Text] = None,
        user_id: Optional[Text] = None,
        parse_data: Dict[Text, Any] = None,
        input_channel: Text = None,
        message_id: Text = None,
    ) -> None:
        self.text = text.strip() if text else text

        if message_id is not None:
            self.message_id = str(message_id)
        else:
            self.message_id = uuid.uuid4().hex

        if output_channel is not None:
            self.output_channel = output_channel
        else:
            self.output_channel = CollectingOutputChannel()
        
        if sender_id is not None:
            self.sender_id = str(sender_id)
        else:
            self.sender_id = self.DEFAULT_SENDER_ID
        
        if request_id is not None:
            self.request_id = str(request_id)
        else:
            self.request_id = self.DEFAULT_REQUEST_ID

        if user_id is not None:
            self.user_id = str(user_id)
        else:
            self.user_id = self.DEFAULT_USER_ID
            
        self.input_channel = input_channel

        self.parse_data = parse_data


def register(
    input_channels: List["InputChannel"], app: Sanic, route: Optional[Text]
) -> None:
    async def handler(*args, **kwargs):
        await app.agent.handle_message(*args, **kwargs)

    for channel in input_channels:
        if route:
            p = urljoin(route, channel.url_prefix())
        else:
            p = None
        app.blueprint(channel.blueprint(handler), url_prefix=p)


def button_to_string(button, idx=0):
    """Create a string representation of a button."""

    title = button.pop("title", "")

    if "payload" in button:
        payload = " ({})".format(button.pop("payload"))
    else:
        payload = ""

    # if there are any additional attributes, we append them to the output
    if button:
        details = " - {}".format(json.dumps(button, sort_keys=True))
    else:
        details = ""

    button_string = "{idx}: {title}{payload}{details}".format(
        idx=idx + 1, title=title, payload=payload, details=details
    )

    return button_string


def element_to_string(element, idx=0):
    """Create a string representation of an element."""

    title = element.pop("title", "")

    element_string = "{idx}: {title} - {element}".format(
        idx=idx + 1, title=title, element=json.dumps(element, sort_keys=True)
    )

    return element_string


class InputChannel(object):
    @classmethod
    def name(cls):
        """Every input channel needs a name to identify it."""
        return cls.__name__

    @classmethod
    def from_credentials(cls, credentials):
        return cls()

    def url_prefix(self):
        return self.name()

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        """Defines a Sanic blueprint.

        The blueprint will be attached to a running sanic server and handle
        incoming routes it registered for."""
        raise NotImplementedError("Component listener needs to provide blueprint.")

    @classmethod
    def raise_missing_credentials_exception(cls):
        raise Exception(
            "To use the {} input channel, you need to "
            "pass a credentials file using '--credentials'. "
            "The argument should be a file path pointing to "
            "a yml file containing the {} authentication "
            "information. Details in the docs: "
            "{}/user-guide/messaging-and-voice-channels/".format(
                cls.name(), cls.name(), DOCS_BASE_URL
            )
        )


class OutputChannel(object):
    """Output channel base class.

    Provides sane implementation of the send methods
    for text only output channels."""

    @classmethod
    def name(cls):
        """Every output channel needs a name to identify it."""
        return cls.__name__

    async def send_response(self, recipient_id: Text, request_id: Text, user_id: Text, message: Dict[Text, Any]) -> None:
        """Send a message to the client."""

        if message.get("quick_replies"):
            await self.send_quick_replies(
                recipient_id,
                request_id, 
                user_id,
                message.pop("text"),
                message.pop("quick_replies"),
                **message
            )
        elif message.get("buttons"):
            await self.send_text_with_buttons(
                recipient_id, request_id, user_id, message.pop("text"), message.pop("buttons"), **message
            )
        elif message.get("text"):
            await self.send_text_message(recipient_id, request_id, user_id, message.pop("text"), **message)
        
        if message.get("custom"):  
            await self.send_custom_json(recipient_id, request_id, user_id, message.pop("custom"), **message)

        # if there is an image we handle it separately as an attachment
        if message.get("image"):
            await self.send_image_url(recipient_id, request_id, user_id, message.pop("image"), **message)

        if message.get("attachment"):
            await self.send_attachment(
                recipient_id, request_id, user_id, message.pop("attachment"), **message
            )

        if message.get("elements"):
            await self.send_elements(recipient_id, request_id, user_id, message.pop("elements"), **message)

        if message.get("parse_data"):
            await self.send_nlu_data(recipient_id, request_id, user_id, parse_data=message.pop("parse_data"), **message)
        

    async def send_nlu_data(
        self, recipient_id: Text, request_id: Text, user_id: Text, parse_data: Dict[Text, Any], **kwargs: Any
    ) -> None:
        """Send parsed NLU data through this channel."""

        await self.send_text_message(recipient_id, request_id, user_id, "nlu: {}".format(parse_data), **kwargs)

    async def send_text_message(
        self, recipient_id: Text, request_id: Text, user_id: Text, text: Text, **kwargs: Any
    ) -> None:
        """Send a message through this channel."""

        raise NotImplementedError(
            "Output channel needs to implement a send message for simple texts."
        )

    async def send_image_url(
        self, recipient_id: Text, request_id: Text, user_id: Text, image: Text, **kwargs: Any
    ) -> None:
        """Sends an image. Default will just post the url as a string."""

        await self.send_text_message(recipient_id, request_id, user_id, "Image: {}".format(image), **kwargs)

    async def send_attachment(
        self, recipient_id: Text, request_id: Text, user_id: Text, attachment: Text, **kwargs: Any
    ) -> None:
        """Sends an attachment. Default will just post as a string."""

        await self.send_text_message(
            recipient_id, request_id, user_id, "Attachment: {}".format(attachment), **kwargs
        )

    async def send_text_with_buttons(
        self,
        recipient_id: Text,
        request_id: Text, 
        user_id: Text,
        text: Text,
        buttons: List[Dict[Text, Any]],
        **kwargs: Any
    ) -> None:
        """Sends buttons to the output.

        Default implementation will just post the buttons as a string."""

        await self.send_text_message(recipient_id, request_id, user_id, text, **kwargs)
        for idx, button in enumerate(buttons):
            button_msg = button_to_string(button, idx)
            await self.send_text_message(recipient_id, request_id, user_id, button_msg, **kwargs)

    async def send_quick_replies(
        self,
        recipient_id: Text,
        request_id: Text, 
        user_id: Text,
        text: Text,
        quick_replies: List[Dict[Text, Any]],
        **kwargs: Any
    ) -> None:
        """Sends quick replies to the output.

        Default implementation will just send as buttons."""

        await self.send_text_message(recipient_id, request_id, user_id, text, **kwargs)
        for idx, quick_reply in enumerate(quick_replies):
            quick_reply_msg = button_to_string(quick_reply, idx)
            await self.send_text_message(recipient_id, request_id, user_id, quick_reply_msg, **kwargs)

    async def send_elements(
        self, recipient_id: Text, request_id: Text, user_id: Text, elements: Iterable[Dict[Text, Any]], **kwargs: Any
    ) -> None:
        """Sends elements to the output."""
                    
        await self.send_text_message(recipient_id, request_id, user_id, json.dumps(elements), **kwargs)
        
    async def send_custom_json(
        self, recipient_id: Text, request_id: Text, user_id: Text, json_message: Dict[Text, Any], **kwargs: Any
    ) -> None:
        """Sends json dict to the output channel.

        Default implementation will just post the json contents as a string."""

        await self.send_text_message(recipient_id, request_id, user_id, json.dumps(json_message), **kwargs)


class CollectingOutputChannel(OutputChannel):
    """Output channel that collects send messages in a list

    (doesn't send them anywhere, just collects them)."""

    def __init__(self):
        self.messages = []

    @classmethod
    def name(cls):
        return "collector"

    @staticmethod
    def _message(
        recipient_id, request_id=UserMessage.DEFAULT_REQUEST_ID, user_id=UserMessage.DEFAULT_USER_ID, text=None, image=None, buttons=None, attachment=None, custom=None, elements=None, quick_replies=None, parse_data=None,
    ):
        """Create a message object that will be stored."""

        obj = {
            "sender_id": recipient_id,
            "request_id": request_id,
            "user_id": user_id,
            "text": text,
            "image": image,
            "buttons": buttons,
            "attachment": attachment,
            "custom": custom,
            "elements": elements,
            "quick_replies": quick_replies,
            "nlu_data": parse_data,
        }

        # filter out any values that are `None`
        return utils.remove_none_values(obj)

    def latest_output(self):
        if self.messages:
            return self.messages[-1]
        else:
            return None

    async def _persist_message(self, message) -> None:
        self.messages.append(message)  # pytype: disable=bad-return-type

    async def send_text_message(
        self, recipient_id: Text, request_id: Text, user_id: Text, text: Text, **kwargs: Any
    ) -> None:
        for message_part in text.split("\n\n"):
            await self._persist_message(self._message(recipient_id, request_id, user_id, text=message_part))

    async def send_nlu_data(
        self, recipient_id: Text, request_id: Text, user_id: Text, parse_data: Dict[Text, Any], **kwargs: Any
    ) -> None:
        """Sends an image. Default will just post the url as a string."""
        await self._persist_message(self._message(recipient_id, request_id, user_id, parse_data=parse_data))

    async def send_image_url(
        self, recipient_id: Text, request_id: Text, user_id: Text, image: Text, **kwargs: Any
    ) -> None:
        """Sends an image. Default will just post the url as a string."""

        await self._persist_message(self._message(recipient_id, request_id, user_id, image=image))

    async def send_attachment(
        self, recipient_id: Text, request_id: Text, user_id: Text, attachment: Text, **kwargs: Any
    ) -> None:
        """Sends an attachment. Default will just post as a string."""

        await self._persist_message(self._message(recipient_id, request_id, user_id, attachment=attachment))

    async def send_text_with_buttons(
        self,
        recipient_id: Text,
        request_id: Text, 
        user_id: Text,
        text: Text,
        buttons: List[Dict[Text, Any]],
        **kwargs: Any
    ) -> None:
        await self._persist_message(
            self._message(recipient_id, request_id, user_id, text=text, buttons=buttons)
        )

    async def send_custom_json(
        self, recipient_id: Text, request_id: Text, user_id: Text, json_message: Dict[Text, Any], **kwargs: Any
    ) -> None:
        await self._persist_message(self._message(recipient_id, request_id, user_id, custom=json_message))

    async def send_elements(
        self, recipient_id: Text, request_id: Text, user_id: Text, elements, **kwargs: Any
    ) -> None:
        await self._persist_message(self._message(recipient_id, request_id, user_id, elements=elements))

    async def send_quick_replies(
        self,
        recipient_id: Text,
        request_id: Text, 
        user_id: Text,
        text: Text,
        quick_replies: List[Dict[Text, Any]],
        **kwargs: Any
    ) -> None:
        await self._persist_message(
            self._message(recipient_id, request_id, user_id, text=text, quick_replies=quick_replies)
        )


class QueueOutputChannel(CollectingOutputChannel):
    """Output channel that collects send messages in a list

    (doesn't send them anywhere, just collects them)."""

    @classmethod
    def name(cls):
        return "queue"

    # noinspection PyMissingConstructor
    def __init__(self, message_queue: Optional[Queue] = None) -> None:
        super(QueueOutputChannel, self).__init__()
        self.messages = Queue() if not message_queue else message_queue

    def latest_output(self):
        raise NotImplementedError("A queue doesn't allow to peek at messages.")

    async def _persist_message(self, message) -> None:
        await self.messages.put(message)  # pytype: disable=bad-return-type


class RestInput(InputChannel):
    """A custom http input channel.

    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa Core and
    retrieve responses from the agent."""

    @classmethod
    def name(cls):
        return "rest"

    @staticmethod
    async def on_message_wrapper(
        on_new_message: Callable[[UserMessage], Awaitable[None]],
        text: Text,
        queue: Queue,
        sender_id: Text,
        request_id: Text,
        user_id: Text,
    ) -> None:
        collector = QueueOutputChannel(queue)

        message = UserMessage(
            text, collector, sender_id, request_id, user_id, input_channel=RestInput.name()
        )
        await on_new_message(message)

        await queue.put("DONE")  # pytype: disable=bad-return-type

    async def _extract_sender(self, req) -> Optional[Text]:
        return req.json.get("sender", None)

    async def _extract_request_id(self, req) -> Optional[Text]:
        return req.json.get("request_id", None)

    async def _extract_user_id(self, req) -> Optional[Text]:
        return req.json.get("user_id", None)
        
    # noinspection PyMethodMayBeStatic
    def _extract_message(self, req):
        return req.json.get("message", None)

    def stream_response(
        self,
        on_new_message: Callable[[UserMessage], Awaitable[None]],
        text: Text,
        sender_id: Text,
        request_id: Text, 
        user_id: Text,
    ) -> Callable[[Any], Awaitable[None]]:
        async def stream(resp: Any) -> None:
            q = Queue()
            task = asyncio.ensure_future(
                self.on_message_wrapper(on_new_message, text, q, sender_id)
            )
            while True:
                result = await q.get()  # pytype: disable=bad-return-type
                if result == "DONE":
                    break
                else:
                    await resp.write(json.dumps(result) + "\n")
            await task

        return stream  # pytype: disable=bad-return-type

    def blueprint(self, on_new_message: Callable[[UserMessage], Awaitable[None]]):
        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        # noinspection PyUnusedLocal
        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request):
            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request):
            sender_id = await self._extract_sender(request)
            request_id = await self._extract_request_id(request)
            user_id = await self._extract_user_id(request)
            
            if not request_id:
                request_id = UserMessage.DEFAULT_REQUEST_ID
                # return response.json(
                #                     {
                #                      "error": {
                #                       "status": 400,
                #                       "message": "Bad Request. Request ID key (request_id) is not found."
                #                      }
                #                     })

            if not user_id:
                user_id = UserMessage.DEFAULT_USER_ID
                # return response.json(
                #                     {
                #                      "error": {
                #                       "status": 400,
                #                       "message": "Bad Request. User ID key (user_id) is not found."
                #                      }
                #                     })

            text = self._extract_message(request)
            should_use_stream = rasa.utils.endpoints.bool_arg(
                request, "stream", default=False
            )

            if should_use_stream:
                return response.stream(
                    self.stream_response(on_new_message, text, sender_id, request_id, user_id),
                    content_type="text/event-stream",
                )
            else:
                collector = CollectingOutputChannel()
                # noinspection PyBroadException
                try:
                    await on_new_message(
                        UserMessage(
                            text, collector, sender_id, request_id, user_id, input_channel=self.name()
                        )
                    )
                except CancelledError:
                    logger.error(
                        "Message handling timed out for "
                        "user message '{}'.".format(text)
                    )
                except Exception:
                    logger.exception(
                        "An exception occured while handling "
                        "user message '{}'.".format(text)
                    )


                response_msg = dict()
                response_msg['sender_id'] = None
                response_msg['request_id'] = None
                response_msg['user_id'] = None
                response_msg['nlu_data'] = {
                                                "text": None,
                                                "intent": {
                                                    "name": None,
                                                    "confidence": 0.0
                                                },
                                                "intent_ranking": [],
                                                "entities": []
                                            }
                response_msg['custom'] = None
                response_msg['data'] = []
                response_msg['elements'] = []
                response_msg['attachments'] = []

                data = []

                for msg in collector.messages:
                    bot_response = dict()
                    bot_response['text'] = None
                    bot_response['buttons'] = []
                    bot_response['quick_replies'] = []
                        
                    if msg.get('text', None) and msg.get('buttons', None):
                        bot_response['text'] = msg.pop('text')
                        button = msg.pop('buttons')
                        if button:
                            bot_response['buttons'] = button
                    elif msg.get('text', None) and msg.get('quick_replies', None):
                        bot_response['text'] = msg.pop('text')
                        quick_reply = msg.pop('quick_replies')
                        if quick_reply:
                            bot_response['quick_replies'] = quick_reply
                    elif msg.get('text', None):
                        bot_response['text'] = msg.pop('text')


                    if bot_response['text']:
                        hash_object = hashlib.md5(bot_response['text'].encode('utf-8'))
                        bot_response["hash"]=str(hash_object.hexdigest())
                        data.append(bot_response)

                    if msg.get('sender_id', None) and not response_msg['sender_id']:
                        response_msg['sender_id'] = msg.pop('sender_id')

                    if msg.get('request_id', None) and not response_msg['request_id']:
                        response_msg['request_id'] = msg.pop('request_id')

                    if msg.get('user_id', None) and not response_msg['user_id']:
                        response_msg['user_id'] = msg.pop('user_id')

                    if msg.get('nlu_data', None) and not response_msg['nlu_data']['text']:
                        response_msg['nlu_data'] = msg.pop('nlu_data')

                    if msg.get('custom', None) and not response_msg['custom']:
                        response_msg['custom'] = msg.pop('custom')

                    if msg.get('elements', None) and len(response_msg['elements']) == 0:
                        response_msg['elements'] = msg.pop('elements')

                    if msg.get('attachments', None) and len(response_msg['attachments']) == 0:
                        response_msg['attachments'] = msg.pop('attachments')


                response_msg['data'] = data
                if not response_msg['custom']:
                    response_msg['custom'] = DEFAULT_CUSTOM_MESSAGE

                return response.json(response_msg)

        return custom_webhook