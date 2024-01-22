# from flask import Flask, request, abort
# from linebot import LineBotApi, WebhookHandler
# from linebot.v3.exceptions import InvalidSignatureError
# from linebot.models import *
# import os, re, json, requests
# from flask_mysqldb import MySQL
# from PIL import Image
# from io import BytesIO
# from imgurpython import ImgurClient
# from datetime import datetime
# import matplotlib

# app = Flask(__name__)
# mysql = MySQL(app)

# imgur_client_id = "980ec226412b95e"
# imgur_client_secret = "a7e432b4827f48c28ce5642bebea3a8c65f753c1"
# imgur_access_token = "412b87ea68ecab734b84985d38a425f5e56623e1"
# imgur_refresh_token = ""

# imgur_client = ImgurClient(imgur_client_id, imgur_client_secret, imgur_access_token, imgur_refresh_token)

# app.config['MYSQL_HOST'] = '3.136.127.234'
# app.config['MYSQL_USER'] = 'project'
# app.config['MYSQL_PASSWORD'] = '3dbuffet'
# app.config['MYSQL_DB'] = '3d_buffet'

# # channel access token
# line_bot_api = LineBotApi('FU7rnaQ3WEnkga5EmyybMMfmG3W5pY24NSpAiKNmr7nfPWyItVVskOEFvD/ppfQquNyNQVG/GlY/KlfPKuQczYlFBMjrJKrppznAGQfLfbJ6fCT3lxU6PnRXzcHlRh2rqoztDCiKgN3E9A98w6IlQwdB04t89/1O/w1cDnyilFU=')
# # channel secret
# handler = WebhookHandler('dd8320ea636f1197e7092a472406874b')
# # line_bot_api.push_message('U3415062f3d7a2a948221e2cd1955954a', TextSendMessage(text="you can start!"))

# @app.route("/callback", methods=['POST'])
# def callback():
#     signature = request.headers['X-Line-Signature']
#     body = request.get_data(as_text=True)

#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#     return 'OK'

# @handler.add(FollowEvent)
# def handle_follow(event):
#     user_line_id = event.source.user_id
#     # 判斷使用者的 line id 有沒有在 database 裡面，沒有才新增，連同 RFID 一起新增
#     print(user_line_id)
#     add_user_info2database(user_line_id)
#     print(f"Received follow from user {user_line_id}")

# def add_user_info2database(user_id):
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute(f"INSERT INTO interface_user (user_line) VALUES ('{user_id}');")
#         mysql.connection.commit()
#         cur.close()
#         print(f"user line id {user_id} added to the database successfully.")
#     except Exception as e:
#         print(f"error adding user to the database: {e}")





# import requests
# import matplotlib.pyplot as plt
# from io import BytesIO
# import numpy as np

# food_name = ['afsadfsf', 'bfsdfasf', 'csfsadf', 'dsfsafds', 'sfjsadlkfjsad']
# weight_result = [0.2, 0.3, 0.4, 0.5, 0.6]
# calorie_result = [0.3, 0.5, 0.3, 0.5, 0.3]
# protein_result = [0.4, 0.5, 0.6, 0.7, 0.8]
# carbohydrate_result = [0.5, 0.7, 0.5, 0.7, 0.5]
# fat_result = [0.6, 0.7, 0.8, 0.9, 1.0]

# data = [weight_result, calorie_result, protein_result, carbohydrate_result, fat_result]
# row_labels = food_name
# col_labels = ['Weight(g)', 'Calories(Kcal)', 'Protein(g)', 'Carbohydrates(g)', 'Fat(g)']

# fig, ax2 = plt.subplots()

# # Hide axes
# ax2.axis('off')
# ax2.axis('tight')

# # Change background color
# fig.patch.set_facecolor('xkcd:light grey')
# # ax2.set_facecolor('xkcd:light grey')

# # Table from data
# table = ax2.table(cellText=data, rowLabels=row_labels, colLabels=col_labels, cellLoc='center', loc='center')

# # Make col_labels (table headers) bold
# for (i, label) in enumerate(col_labels):
#     table[0, i].get_text().set_fontweight('bold')

# # Change cell color
# cells = table.properties()["children"]
# for cell in cells:
#     # cell.set_facecolor('xkcd:light blue')
#     cell.set_facecolor('#AEDFE0')
#     cell.set_edgecolor('white')

# # Adjust column widths
# table.auto_set_column_width(col=list(range(len(col_labels))))
# table.auto_set_font_size(False)
# table.set_fontsize(10)
# table.scale(1, 2)  # change the second parameter to adjust row height

# plt.show()

# buffer = BytesIO()
# plt.savefig(buffer, format='png', bbox_inches='tight')
# buffer.seek(0)

# def upload_image(img_data, imgur_token):
#     headers = {'Authorization': f'Bearer {imgur_token}',}

#     # # 將照片讀取為二進制數據
#     # with open(img_path, 'rb') as img_file:
#     #     img_data = img_file.read()

#     # 設定上傳的 URL
#     upload_url = 'https://api.imgur.com/3/upload'

#     # 設定上傳的參數
#     upload_params = {
#         'image': img_data.getvalue(),
#     }

#     # 發送 POST 請求進行上傳
#     response = requests.post(upload_url, headers=headers, files=upload_params)

#     # 解析 API 回應
#     if response.status_code == 200:
#         data = response.json()
#         link = data['data']['link']
#         print(f'照片上傳成功！連結：{link}')

#         # 回傳 Imgur 照片的連結
#         return link
#     else:
#         print(f'照片上傳失敗。錯誤碼：{response.status_code}')
#         return None

# # 替換成您的照片檔案路徑和 Imgur Token

# imgur_token = '412b87ea68ecab734b84985d38a425f5e56623e1'

# # 上傳照片並獲取 Imgur 照片的連結
# imgur_link = upload_image(buffer, imgur_token)

# if imgur_link:
#     print(f'Imgur 照片的連結為：{imgur_link}')





show = [['新貴派', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], ['oreo', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], ['yuki', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], ['雪餅', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], ['旺旺仙貝', 83.88, 399.83, 3.64, 62.63, 15.11, 25.95], ['黑麥口糧', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
with open('merged_data.txt', 'w') as file:
    for item in show:
        # 使用过滤器保留只是数字的部分
        numeric_values = [str(value) for value in item if isinstance(value, (int, float))]
        file.write(','.join(numeric_values) + '\n')
