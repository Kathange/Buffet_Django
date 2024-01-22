from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os, re
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_HOST'] = '3.136.127.234'
app.config['MYSQL_USER'] = 'project'
app.config['MYSQL_PASSWORD'] = '3dbuffet'
app.config['MYSQL_DB'] = '3d_buffet'

# channel access token
line_bot_api = LineBotApi('FU7rnaQ3WEnkga5EmyybMMfmG3W5pY24NSpAiKNmr7nfPWyItVVskOEFvD/ppfQquNyNQVG/GlY/KlfPKuQczYlFBMjrJKrppznAGQfLfbJ6fCT3lxU6PnRXzcHlRh2rqoztDCiKgN3E9A98w6IlQwdB04t89/1O/w1cDnyilFU=')
# channel secret
handler = WebhookHandler('dd8320ea636f1197e7092a472406874b')
user_input_status = {}

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
    # print(user_line_id)
    add_user_info2database(user_line_id)
    # print(f"Received follow from user {user_line_id}")

@handler.add(PostbackEvent)
def handle_postback(event):
    postback_data = event.postback.data
    userLine = event.source.user_id
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT user_id FROM interface_user WHERE user_line = \"{userLine}\"")
    user_id_result = cursor.fetchone()
    
    if postback_data == 'action=search_date':
        date_picker = DatetimePickerTemplateAction(
            label="選擇日期",  # 按鈕的文字
            data="action=select_date",  # 用於接收日期選擇器回傳的數據
            mode="date",  # 選擇器模式，此處為日期模式
        )

        buttons_template = ButtonsTemplate(
            text="請選擇要查詢的日期",
            actions=[date_picker],
        )

        template_message = TemplateSendMessage(
            alt_text="日期選擇器",
            template=buttons_template,
        )

        line_bot_api.reply_message(event.reply_token, template_message)
        
    elif postback_data == 'action=search_duration':
        start_date_picker = DatetimePickerTemplateAction(
            label="起始日期",
            data="action=select_start_date",
            mode="date",
        )

        # 結束日期選擇器
        end_date_picker = DatetimePickerTemplateAction(
            label="結束日期",
            data="action=select_end_date",
            mode="date",
        )

        # 按鈕模板包含起始與結束日期選擇器
        buttons_template = ButtonsTemplate(
            text="請選擇日期區間",
            actions=[start_date_picker, end_date_picker],
        )

        # 建立模板訊息
        template_message = TemplateSendMessage(
            alt_text="日期區間選擇器",
            template=buttons_template,
        )
        line_bot_api.reply_message(event.reply_token, template_message)
    elif postback_data == 'action=select_date':
        selected_date = event.postback.params['date']

        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT food_img, donut_chart_img, sheet_img, eat_date, eat_time, total_cal FROM interface_record WHERE eat_date = '{selected_date}' AND user_id = {user_id_result[0]};")
        a_history_record_result = cursor.fetchall()
        cursor.close()

        if len(a_history_record_result) == 0:
            line_bot_api.reply_message(event.reply_token, TextMessage(text=f"您那天沒有用餐"))
        else:
            message_reply = []
            for i in range(len(a_history_record_result)):
                message_reply.append(
                    ImageSendMessage(
                        original_content_url = a_history_record_result[i][0], # 要輸出的圖
                        preview_image_url = a_history_record_result[i][0]
                    )
                )
                message_reply.append(
                    ImageSendMessage(
                        original_content_url = a_history_record_result[i][1],
                        preview_image_url = a_history_record_result[i][1]
                    )
                )
                message_reply.append(
                    ImageSendMessage(
                        original_content_url = a_history_record_result[i][2],
                        preview_image_url = a_history_record_result[i][2]
                    )
                )
                line_bot_api.reply_message(event.reply_token, message_reply)
    elif postback_data.startswith('action=select_start_date'):
        selected_start_date = event.postback.params['date']
        user_input_status[event.source.user_id] = {'start_date': selected_start_date}
        # 回覆使用者選擇的起始日期
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"請接著選擇結束日期")
        )

    elif postback_data.startswith('action=select_end_date'):
        if event.source.user_id in user_input_status and 'start_date' in user_input_status[event.source.user_id]:
            selected_end_date = event.postback.params['date']
            user_input_status[event.source.user_id]['end_date'] = selected_end_date
            start_date = user_input_status[event.source.user_id]['start_date']
            end_date = user_input_status[event.source.user_id]['end_date']
            
            cur = mysql.connection.cursor()
            cur.execute(f"SELECT eat_date, eat_time, total_cal FROM interface_record WHERE eat_date BETWEEN '{start_date}' AND '{end_date}' AND user_id = {user_id_result[0]}")
            info_result = cur.fetchall()
            cur.close()
            
            text = ""
            for i in range(len(info_result)):
                text += f"您在{info_result[i][0]} {info_result[i][1]}食用了{info_result[i][2]}(cal)\n"
            if len(text) != 0:
                text += f"欲查詢詳細資訊請輸入單個日期"
            else:
                text += f"您這段時間沒有用餐"
            line_bot_api.reply_message(event.reply_token,TextMessage(text=text))
    
            # 清除使用者輸入狀態
            del user_input_status[event.source.user_id]
        else:
            # 如果使用者還未選擇起始日期，可以回應提醒使用者先選擇起始日期
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="請先選擇起始日期")
            )

    # 如果使用者只選了一個日期或輸入了其他資訊，您可以在這裡處理該情況
    else:
        pass

# @handler.add(MessageEvent)
# def handle_trigger(event):
#     user_line_id = event.source.user_id
#     record_id = event.record_id
#     message = f"New record inserted with ID: {user_line_id}"

#     print(f"user_line_id: {user_line_id}, record_id: {record_id}, message: {message}")

# handler 要改成trigger的方式
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    1. 透過新新增的 record_id 去得到 user_id, eat_time, eat_date, food_img, total_cal
    2. 透過得到的 user_id 去取得 user_line
       透過 user_id 與 user_line 得到 food_id, weight, calorie, protein, carbohydrate, fat
       透過 food_id 得到 name
    3. 將上述資訊合起來計算環圈圖還有製作分項表格, 再透過 imgur api 將圖片上傳到 imgur 並取得 url
       透過 reocrd_id user_id 將 url 存到 database
    4. 透過 user_line 將環圈圖, 食物圖, 表格傳到 line 裡面
    """
    message = event.message.text
    user_line = event.source.user_id

    # 獲取 user_line
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT user_id FROM interface_user WHERE user_line = \"{user_line}\"")
    user_id_result = cursor.fetchone()
    cursor.close()

    if re.match("test", message):
        # # 獲取 record_id
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT record_id FROM interface_record WHERE user_id = {user_id_result[0]} ORDER BY record_id DESC LIMIT 1;")
        record_id_result = cursor.fetchone()
        cursor.close()

        # 獲取單筆 record 的 info
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT food_img, eat_date, eat_time, total_cal, donut_chart_img, sheet_img from interface_record where record_id = {record_id_result[0]};")
        a_record_result = cur.fetchone()
        cur.close()

        try:
            message_reply = [
            TextMessage(text=f"您在{a_record_result[1]} {a_record_result[2]}食用了{a_record_result[3]}(cal)，以下是您這餐的詳細資訊"),
            ImageSendMessage(
                original_content_url = a_record_result[0], # 要輸出的圖
                preview_image_url = ""
            ),
            ImageSendMessage(
                original_content_url = f"\'{a_record_result[4]}\'",
                preview_image_url = ""
            ),
            ImageSendMessage(
                original_content_url = f"\'{a_record_result[5]}\'",
                preview_image_url = ""
            )]
            line_bot_api.reply_message(event.reply_token, message_reply)
        except Exception as e:
            print(f"error: {e}")
    
def add_user_info2database(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"UPDATE interface_user SET user_line = \'{user_id}\' WHERE user_line IS NULL;")
        mysql.connection.commit()
        cur.close()
        # print(f"user line id {user_id} added to the database successfully.")
    except Exception as e:
        print(f"error adding user to the database: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)