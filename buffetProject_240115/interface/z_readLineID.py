from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.models import *
import os, re, json, requests
from flask_mysqldb import MySQL
from PIL import Image
from io import BytesIO
from imgurpython import ImgurClient
from datetime import datetime
import matplotlib

app = Flask(__name__)
mysql = MySQL(app)

imgur_client_id = "980ec226412b95e"
imgur_client_secret = "a7e432b4827f48c28ce5642bebea3a8c65f753c1"
imgur_access_token = "412b87ea68ecab734b84985d38a425f5e56623e1"
imgur_refresh_token = ""

imgur_client = ImgurClient(imgur_client_id, imgur_client_secret, imgur_access_token, imgur_refresh_token)

app.config['MYSQL_HOST'] = '3.136.127.234'
app.config['MYSQL_USER'] = 'project'
app.config['MYSQL_PASSWORD'] = '3dbuffet'
app.config['MYSQL_DB'] = '3d_buffet'

# channel access token
line_bot_api = LineBotApi('FU7rnaQ3WEnkga5EmyybMMfmG3W5pY24NSpAiKNmr7nfPWyItVVskOEFvD/ppfQquNyNQVG/GlY/KlfPKuQczYlFBMjrJKrppznAGQfLfbJ6fCT3lxU6PnRXzcHlRh2rqoztDCiKgN3E9A98w6IlQwdB04t89/1O/w1cDnyilFU=')
# channel secret
handler = WebhookHandler('dd8320ea636f1197e7092a472406874b')
# line_bot_api.push_message('U3415062f3d7a2a948221e2cd1955954a', TextSendMessage(text="you can start!"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(FollowEvent)
def handle_follow(event):
    user_line_id = event.source.user_id
    # 判斷使用者的 line id 有沒有在 database 裡面，沒有才新增，連同 RFID 一起新增
    print(user_line_id)
    add_user_info2database(user_line_id)
    print(f"Received follow from user {user_line_id}")

def add_user_info2database(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO interface_user (user_line) VALUES ('{user_id}');")
        mysql.connection.commit()
        cur.close()
        print(f"user line id {user_id} added to the database successfully.")
    except Exception as e:
        print(f"error adding user to the database: {e}")


