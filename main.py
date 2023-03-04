from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import os
import requests
import pprint
import urllib.request
from bs4 import BeautifulSoup


import scw    #先ほどファイルをインポート

app=Flask(__name__)
#環境変数の取得
YOUR_CHANNEL_SECRET = "63d4fc0f5af7948c6658ab08b6a32c4b"
YOUR_CHANNEL_ACCESS_TOKEN = "C/R9zrByu/3DDFMEaGI8gV+XQePJV1ZC5ApLbHzVBuhqNCMLjMLrL6s+MuZs+Prl6Qu1hh9LdSlgz746Xzfaa8pnTeweyb5FeSHFByr+m31IcHUVLQZw5agbb+swmH2GnRx7mO8n8yOadl6rt7GHdwdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

#テスト用
@app.route("/")
def hello_world():
   return "cheer up!!2"

@app.route("/callback",methods=["POST"])
def callback():
    signature=request.headers["X-Line-Signature"]

    body=request.get_data(as_text=True)
    app.logger.info("Request body"+body)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    #user_idを取得
    get_user_id = line_bot_api.get_profile(event.source.user_id)
    
    #入力された文字を取得
    text_in = event.message.text

    if "今日" in text_in:   #scw.pyのgetw関数を呼び出している
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=scw.getw()))
        #画像用意
        main_image_path = f"static/images/marimo_sunny.png"
        preview_image_path = f"static/images/marimo_sunny.png"
        #送信
        image_message = ImageSendMessage(
            original_content_url=f"https://line-bot-sou23-git-1.onrender.com/{main_image_path}",
            preview_image_url=f"https://line-bot-sou23-git-1.onrender.com/{preview_image_path}",
        )
        line_bot_api.push_message(get_user_id,messages=image_message)
    elif "明日" in text_in:   #scw.pyのtom_getw関数を呼び出している
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=scw.tom_getw()))

    else:   #「今日」「明日」以外の文字はオウム返しする
     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))



if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)

#line_bot_api.push_message(event.source.user_id, ImageSendMessage(image='marimo_sunny.jpg'))
#https://github.com/sou23-git/line-bot-test/blob/main/images/marimo_sunny.png