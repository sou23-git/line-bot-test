from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

import os

app = Flask(__name__)

# チャネルシークレットを設定
YOUR_CHANNEL_SECRET = "63d4fc0f5af7948c6658ab08b6a32c4b"
# チャネルアクセストークンを設定
YOUR_CHANNEL_ACCESS_TOKEN = "C/R9zrByu/3DDFMEaGI8gV+XQePJV1ZC5ApLbHzVBuhqNCMLjMLrL6s+MuZs+Prl6Qu1hh9LdSlgz746Xzfaa8pnTeweyb5FeSHFByr+m31IcHUVLQZw5agbb+swmH2GnRx7mO8n8yOadl6rt7GHdwdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# https://example.herokuapp.com/callback にアクセスされたら以下の関数を実行する
@app.route("/callback", methods=['POST'])
def callback():
    # アクセス時に送られてきたデータ「X-Line-Signature」を代入
    signature = request.headers['X-Line-Signature']

    # アクセス時に送られてきたデータの主な部分を代入
    body = request.get_data(as_text=True)

    # try 内でエラーが発生したら except の文を実行
    try:
        # ハンドラーに定義されている関数を呼び出す
        handler.handle(body, signature)
    # もし「InvalidSigunatureError」というエラーが発生したら、以下のプログラムを実行
    except InvalidSignatureError:
        # リクエストを送った側に400番(悪いリクエストですよー！)を返す
        abort(400)

    # すべて順調にいけば、リクエストを送った側に「OK」と返す
    return "OK"

# ハンドラーに定義されている関数
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ここにメッセージの内容による処理を書いていこう

    # メッセージの種類が「テキスト」なら
    if event.type == "message":
        response_message = ""

        # event.message.text という変数にメッセージの内容が入っている
        if (event.message.text == "おはようございます"):
            response_message = "Good morning!"

        elif (event.message.text == "こんにちは"):
            response_message = "Good afternoon!"

        elif (event.message.text == "こんばんは"):
            response_message = "Good evening!"

        else:
            response_message = "その言葉はわかりません。"

        # 返信文を送信
        # response_message の中に入っている文を返す
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=response_message)
            ]
        )

# ポート番号を環境変数から取得
port = os.getenv("PORT")
app.run(host="0.0.0.0", port=port)
