from __future__ import unicode_literals

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage
import configparser

# LINE 聊天機器人的基本資料
app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    # 請求body作為text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 判斷是否開台
def notification(channel_title, channel_game, channel_streamer):
    line_bot_api.broadcast(TextSendMessage(
        text='開台摟\n開台連結：https://www.twitch.tv/{}\n標題：{}\n遊戲：{}'.format(channel_streamer, channel_title,
                                                                       channel_game)))


# set_interval(notification(), 5)
if __name__ == "__main__":
    app.run()
