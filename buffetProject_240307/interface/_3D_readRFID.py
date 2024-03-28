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
    if request.method == 'GET':
        # time.sleep(0.1)

        serial_port = 'COM7'
        ser = serial.Serial(serial_port, 9600, timeout=1)
        # print("ser: ",ser)
        # print(type(ser))
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

                    flask_url = "https://0a98-60-250-225-149.ngrok-free.app/endpoint"
                    # print(type(uid_value))
                    response = requests.post(flask_url, data={'variable_name':uid_value})
                    if response.status_code == 200:
                        print('success')
                    else:
                        print('failed', response.status_code)

                    if is_duplicate:
                        # ser.close()
                        return JsonResponse({'uid': "none"})
                    
                    # ser.close()
                    return JsonResponse({'uid': uid_value})
                
                # print("check")
                if keyboard.is_pressed('s'):
                    print("serial close")
                    ser.close()
                    return JsonResponse({'uid': "notJoin"})
                
        except KeyboardInterrupt:
            print("Program terminated by user.")
            ser.close()
        finally:
            ser.close()


# 如果來亂的，不加入又掃，就傳訊息把它刪了
def onclick():
    flask_url = "https://0a98-60-250-225-149.ngrok-free.app/deleteData"
    response = requests.post(flask_url, data={'delete_data':"1"})
    if response.status_code == 200:
        print('success')
    else:
        print('failed', response.status_code)
    print("onclick in")
    return JsonResponse({'status': 'success'})


