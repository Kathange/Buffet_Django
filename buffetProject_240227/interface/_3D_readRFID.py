"""

此為讀取RFID，並寫入資料庫(還要再改)

"""


from django.http import JsonResponse
import serial
from .models import user
from django.db import connection
import requests
from django.shortcuts import render, redirect
import keyboard
import time


def readRFID(request):
    # # 如果上一個人只掃了rfid而不加瀨，就讓那個rfid從資料庫刪除
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM interface_user WHERE user_line IS NULL;")
    #     User = cursor.fetchall()
    # print(User)
    # if len(User) != 0:
    #     with connection.cursor() as cursor:
    #         cursor.execute(f"DELETE FROM interface_user WHERE user_id = \'{User[0][0]}\';")
    time.sleep(0.1)

    serial_port = 'COM7'
    ser = serial.Serial(serial_port, 9600, timeout=1, bytesize=8, parity='N', stopbits=1)
    # Flag to control the reading loop
    reading_flag = True
    try:
        while reading_flag:
            # 读取串口数据
            line = ser.readline().decode('utf-8').strip()
            # 如果数据包含 "UID Value:"，表示读取到 UID
            if "Card UID:" in line:
                # 提取 UID 部分
                uid_value = line.split(":")[1].strip()
                print(f"Read UID: {uid_value}")
                # Check if UID is a valid number (you may need to customize this validation)
                reading_flag = False
                ser.close()

                # Save merged data to a text file
                with open('./static/file/rfid.txt', 'w') as file:
                    file.write(uid_value)

                # 使用filter查找数据库中具有相同name的项
                rfidExist = user.objects.filter(user_RFID=uid_value)
                # 如果有任何一个项与给定的name匹配，返回True；否则返回False
                is_duplicate = rfidExist.exists()
                
                # if is_duplicate:
                #     # variable_to_send = 'rfidDone'
                #     flask_url = "https://bf01-60-250-225-149.ngrok-free.app/endpoint"
                #     # print(type(uid_value))
                #     response = requests.post(flask_url, data={'variable_name':uid_value})
                #     if response.status_code == 200:
                #         print('success')
                #     else:
                #         print('failed', response.status_code)
                #     ser.close()
                #     return JsonResponse({'uid': 'none', 'flag':True})

                # 知道現在有多少筆資料
                # data_count = user.objects.count()
                # data_count += 1
                # 寫入 user 資料庫
                # userunit = user.objects.create(user_id=data_count+1, user_RFID=uid_value)
                # userunit.save()
                # with connection.cursor() as cursor:
                #     cursor.execute("INSERT INTO interface_user (user_id, user_RFID) VALUES (%s, %s)", [data_count, uid_value])
                # print("insert success!")

                # variable_to_send = 'rfidDone'
                flask_url = "https://7991-61-216-173-3.ngrok-free.app/endpoint"
                # print(type(uid_value))
                response = requests.post(flask_url, data={'variable_name':uid_value})
                if response.status_code == 200:
                    print('success')
                else:
                    print('failed', response.status_code)

                if is_duplicate:
                    return JsonResponse({'uid': "none"})
                
                return JsonResponse({'uid': uid_value})
    except KeyboardInterrupt:
        print("Program terminated by user.")
        ser.close()
    finally:
        # 关闭串口
        ser.close()


# 如果來亂的，不加入又掃，就傳訊息把它刪了
def onclick():
    flask_url = "https://7991-61-216-173-3.ngrok-free.app/deleteData"
    response = requests.post(flask_url, data={'delete_data':"1"})
    if response.status_code == 200:
        print('success')
    else:
        print('failed', response.status_code)
    print("onclick in")
    return JsonResponse({'status': 'success'})


def ultrasound(request):
    # 初始化串口通信
    serial_port = 'COM7'  # 修改为你的串行端口
    ser = serial.Serial(serial_port, 9600, timeout=1)

    time = 10 # 一次0.5sec 用來控制時間
    dis = 100 # 用來控制偵測距離 (cm)
    count = 0  # 用于计数连续小于100cm的次数
    try:
        while True:
            # 从串行端口读取一行数据
            line = ser.readline().decode('utf-8').strip()
            if line.startswith("Distance in CM:"):
                # 提取距离值
                distance = int(line.split(":")[1].strip())
                print(f"Detected distance: {distance} cm")  # 打印距离

                # 检查距离是否小于100cm
                if distance < dis:
                    count += 1
                else:
                    count = 0  # 如果距离不小于100cm，重置计数

                # 如果连续超过20次小于100cm，则发送警告
                if count > time:
                    # print("餐盤在這裡待了5秒")
                    # # 在这里执行发送信号的代码
                    # count = 0  # 可选：发送警告后重置计数，避免连续发送警告
                    ser.close()
                    return JsonResponse({'five': 'five'})

    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        ser.close()  # 关闭串行端口



