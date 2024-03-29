import base64
import json
import os
import xml.etree.ElementTree as ET
from .stock_exchange import AlphaVantage
from .graph_generator import *

# Message Styles
SIMPLE = 'simple'
WITH_QUOTE = 'message with QUOTE'
WITH_GRAPH = 'message with GRAPH'


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def msg_format(message, msg_style, entity=None):
    if msg_style == SIMPLE:
        return dict(
            # message=msg_xml
            message="<messageML>"
                    "{}"
                    "</messageML>".format(message),
        )
    elif msg_style == WITH_QUOTE:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '\\message_templates\\quote_card') as my_file:
            string = my_file.read()
            return dict(
                message=string,
                data=json.dumps(entity)
            )
    elif msg_style == WITH_GRAPH:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '\\message_templates\\graph') as my_file:
            string = my_file.read()
            return dict(
                message=string,
                data=json.dumps(entity)
            )


def get_quote(symbol):
    quote = AlphaVantage.get_stock_global_quote(symbol)
    if 'Error Message' in quote:
        msg_to_send = msg_format("Can't seem to find it, are you sure that's the right symbol?", SIMPLE)
    else:
        quote['Global Quote']['change color'] = 'green' \
            if float(quote['Global Quote']['09. change']) > 0 \
            else 'red'
        msg_to_send = msg_format('', WITH_QUOTE, entity=quote)
    return msg_to_send


def get_graph(symbol):
    daily_data = AlphaVantage.get_timeseries_daily(symbol, 'compact')
    if 'Error Message' in daily_data:
        msg_to_send = msg_format("Can't seem to find it, are you sure that's the right symbol?", SIMPLE)
    else:
        plot(daily_data['Time Series (Daily)'])
        with open('..//resources//plot-close.png', 'rb') as graph_image:
            img = graph_image.read()
            img_data = {'graph_img': {
                'symbol': symbol,
                'payload': base64.b64encode(img).decode('utf-8')
            }}
            msg_to_send = msg_format("Here's the graph", WITH_GRAPH, entity=img_data)

    return msg_to_send


def get_symbol_from_msg(incoming_msg, msg_txt):
    txt_array = msg_txt.split()
    symbol = txt_array[len(txt_array) - 1].upper()
    return symbol


class MessageProcessor:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    def process(self, incoming_msg):
        msg_xml = incoming_msg['message']
        msg_root = ET.fromstring(msg_xml)
        msg_txt = msg_root[0].text

        user = incoming_msg['user']

        if "QUOTE" in msg_txt.upper():
            symbol = get_symbol_from_msg(incoming_msg, msg_txt)
            self.send_quote_request_acknowledgement(incoming_msg, symbol)
            msg_to_send = get_quote(symbol)

        elif "GRAPH" or "CHART" in msg_txt.upper():
            symbol = get_symbol_from_msg(incoming_msg, msg_txt)
            self.send_graph_request_acknowledgement(incoming_msg, symbol)
            msg_to_send = get_graph(symbol)

        else:
            msg_to_send = msg_format('Yes {} yes!'.format(user['firstName']), SIMPLE)
            print(msg_to_send)

        if msg_txt:
            self.send_msg(incoming_msg, msg_to_send)

    def send_quote_request_acknowledgement(self, incoming_msg, symbol):
        msg_to_send = msg_format('Ok, wait a bit while I retrieve quote for {}...'.format(symbol), SIMPLE)
        self.send_msg(incoming_msg, msg_to_send)

    def send_graph_request_acknowledgement(self, incoming_msg, symbol):
        msg_to_send = msg_format('Ok, wait a bit while I plot graph for {}...'.format(symbol), SIMPLE)
        self.send_msg(incoming_msg, msg_to_send)

    def send_msg(self, incoming_msg, msg_to_send):
        stream_id = incoming_msg['stream']['streamId']
        self.bot_client.get_message_client(). \
            send_msg(stream_id, msg_to_send)
