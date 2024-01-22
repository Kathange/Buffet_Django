"""

此為讀取RFID，並寫入資料庫(還要再改)

"""


from django.http import JsonResponse
import serial
from .models import user
from django.db import connection
import requests

# import subprocess
# import json

# finfo = []
# def readLineID():
#     script_path = "interface/_3D_readLineID.py"
#     try:
#         print("inin")
#         child_process = subprocess.Popen(["python", script_path],
#                                           stdin = subprocess.PIPE,
#                                           stderr = subprocess.PIPE,
#                                           stdout = subprocess.PIPE,
#                                           text = True)
#         print("123")
#         data = [[1, 2, 3], [4, 5, 6]]
#         input_data = json.dumps(data)
#         input_bytes = input_data.encode()

#         output, error = child_process.communicate(input=input_bytes)
#         # child_process.stdin.write(finfo)
#         print("in")
#         # # 关闭标准输入，通知子进程没有更多数据发送
#         # child_process.stdin.close()
#         # # 等待子进程完成
#         # child_process.wait()
#     except:
#         print(f"subprocess error: {Exception}")
#     finfo.clear()
#     return None

def readRFID(request):
    # # 如果上一個人只掃了rfid而不加瀨，就讓那個rfid從資料庫刪除
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM interface_user WHERE user_line IS NULL;")
    #     User = cursor.fetchall()
    # print(User)
    # if len(User) != 0:
    #     with connection.cursor() as cursor:
    #         cursor.execute(f"DELETE FROM interface_user WHERE user_id = \'{User[0][0]}\';")

    serial_port = 'COM7'
    ser = serial.Serial(serial_port, 9600, timeout=1)
    # Flag to control the reading loop
    reading_flag = True
    try:
        while reading_flag:
            # 读取串口数据
            line = ser.readline().decode('utf-8').strip()
            # 如果数据包含 "UID Value:"，表示读取到 UID
            if "UID Value:" in line:
                # 提取 UID 部分
                uid_value = line.split(":")[1].strip()
                print(f"Read UID: {uid_value}")
                # Check if UID is a valid number (you may need to customize this validation)
                reading_flag = False

                # Save merged data to a text file
                with open('./static/file/rfid.txt', 'w') as file:
                    file.write(uid_value)

                # 使用filter查找数据库中具有相同name的项
                rfidExist = user.objects.filter(user_RFID=uid_value)
                # 如果有任何一个项与给定的name匹配，返回True；否则返回False
                is_duplicate = rfidExist.exists()
                if is_duplicate:
                    ser.close()
                    return JsonResponse({'uid': 'none', 'flag':True})
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
                flask_url = "https://9571-36-231-202-57.ngrok-free.app/endpoint"
                # print(type(uid_value))
                response = requests.post(flask_url, data={'variable_name':uid_value})
                if response.status_code == 200:
                    print('success')
                else:
                    print('failed', response.status_code)

                # readLineID()
                ser.close()
                return JsonResponse({'uid': uid_value, 'flag':False})
    finally:
        # 关闭串口
        ser.close()


# def getUserBool(request):
#     userBool = "none"
#     userBool = request.POST.get('add_database')
#     print(userBool)
#     return 'Thanks'
#     # return JsonResponse({'Thanks': userBool})
