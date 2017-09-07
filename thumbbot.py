import os
import re

from flask import Flask, request, abort
from SendMessageFactory import SendMessageFactory

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)


app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

sendMessageFactory = SendMessageFactory()

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        app.logger.error(e)
        abort(400)

    return 'OK'


# @handler.default()
# def default(event):
#     app.logger.info("default handler: " + event)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    app.logger.info(event.message.text)
    messageObj = sendMessageFactory.getSendMessageInstance(event.message.text)
    app.logger.info(messageObj)

    if messageObj:
        line_bot_api.reply_message(event.reply_token, messageObj)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='懶趴不夠大幹話不嫌少有洞直須插悔叫大懶趴'))

if __name__ == "__main__":
    # app.run(host="0.0.0.0", debug=True) 
    # app.run(host="0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)