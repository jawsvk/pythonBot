from sym_api_client_python.listeners.im_listener import IMListener
from .message_processor import MessageProcessor
import logging


def log_event(comment, message):
    logging.debug(comment, message)


class IMListenerImpl(IMListener):
    def __init__(self, sym_bot_client):
        self.bot_client = sym_bot_client
        self.msg_processor = MessageProcessor(self.bot_client)

    def on_im_created(self, im_created):
        log_event('IM created!', im_created)

    def on_im_message(self, im_message):
        log_event('message received in IM', im_message)
        self.msg_processor.process(im_message)
