from django.shortcuts import render, redirect
from django.http import JsonResponse
import serial
import os
import requests
from interface.models import user, record
from interface._3D_getDB import getDBAllData
from ._3D_Wunetinput import doing
from interface._3D_delete import negativeDelete
from ._3D_WwriteDB import WwriteDB


# Create your views here.
def Wmember(request):
    return render(request, "waste\\Wmember.html")

def Wnegative(request):
    return render(request, "waste\\Wnegative.html")

def WreadRFID(request):
    if request.method == 'GET':
        serial_port = 'COM3'
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

                    if is_duplicate:
                        # ser.close()
                        flask_url = "https://72ea-59-125-186-123.ngrok-free.app/waste"
                        # print(type(uid_value))
                        response = requests.post(flask_url, data={'waste':uid_value})
                        if response.status_code == 200:
                            print('success')
                        else:
                            print('failed', response.status_code)
                        return JsonResponse({'uid': "none"})
                    
                    # ser.close()
                    return JsonResponse({'uid': uid_value})
                
        except KeyboardInterrupt:
            print("Program terminated by user.")
            ser.close()
        finally:
            ser.close()


def Wcamera(request):
    getDBAllData()
    if request.method == 'POST':
        doing()
        # ngrok_url = requests.get("http://127.0.0.1:4040/api/tunnels").json()['tunnels'][0]['public_url']
        # return redirect(f'{ngrok_url}/interface/cashier')
        # return redirect('https://e614-61-218-122-234.ngrok-free.app/interface/cashier')
        return redirect('http://127.0.0.1:8000/waste/Wcashier')
    return render(request, "waste\\Wcamera.html")


def Wcashier(request):
    # 如果體積檔案根本不在，就跳到negative.html
    if not os.path.exists('./static/file/volume.txt'):
        negativeDelete()
        return render(request, 'waste\\Wnegative.html')
    # Read merged data from the text file
    volume_data = []
    # Read data from 'volume.txt'
    with open('./static/file/volume.txt', 'r') as file:
        volume_data = [list(map(float, line.strip().split(','))) for line in file]
    # Flatten the volume_data list to a 1D list
    read_volume = []
    for sublist in volume_data:
        read_volume.extend(sublist)
    # print(read_volume)
    # 如果體積出現負值，就跳到negative.html
    if read_volume[0]<0 or read_volume[1]<0 or read_volume[2]<0:
        negativeDelete()
        return render(request, 'waste\\Wnegative.html')
    
    WwriteDB()
    
    # 讀取RFID
    with open('./static/file/rfid.txt', 'r') as file:
        rfid_data = file.read()
    # 拿取RFID的主人的id
    buyer = user.objects.get(user_RFID=rfid_data)
    record_ori = record.objects.filter(user_line=buyer).last()

    cost = int(round(float(record_ori.cost) - read_volume[0], 0))
    weight = round(float(record_ori.total_weight) - read_volume[1], 3)
    calories = round(float(record_ori.total_cal) - read_volume[2], 3)
    context = {'cost': cost, 'weight': ("%.03f" % weight), 'calories': ("%.03f" % calories)}
    return render(request, "waste\\Wcashier.html", context)

