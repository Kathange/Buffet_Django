from django.shortcuts import render, redirect
from .models import *
from django.http.response import StreamingHttpResponse
from django.http import JsonResponse
import os
import requests
from django.core.exceptions import ObjectDoesNotExist
import time
import keyboard

from ._3D_camera import FoodVedioCamera
from ._3D_getDB import getDBAllData
from ._3D_writeDB import writeDB
from ._3D_unetinput import doing
from ._3D_readRFID import onclick
from ._3D_delete import negativeDelete


    

# 設置 camera (要把模型放進去應該去camera.py寫)
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# 連接攝影機(特定語法，應該，我是複製貼上)，gen(camera.py中的class)
def FoodVedioFeed(request):
    return StreamingHttpResponse(gen(FoodVedioCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
    

# 關於我們的頁面
def about(request):
    return render(request, 'interface\\about.html')

# 加入會員頁面
def joinMember(request):
    return render(request, 'interface\\joinMember.html')

# 開啟攝影機頁面
def camera(request):
    getDBAllData()
    onclick()
    file_path = './static/file/rfid.txt'
    # 檢查檔案是否存在
    if os.path.exists(file_path):
        # 打開檔案 讀取內容
        with open('./static/file/rfid.txt', 'r') as file:
            rfid_data = file.read()
        try:
            buyer = user.objects.get(user_RFID=rfid_data)
            # 如果成功取得 user 物件，這裡執行存在時的動作
            print("in")
        except ObjectDoesNotExist:
            # 如果找不到對應的 user 物件，這裡執行不存在時的動作
            print("camera delete")
            os.remove(file_path)
    else:
        pass

    if request.method == 'POST':
        doing()
        # ngrok_url = requests.get("http://127.0.0.1:4040/api/tunnels").json()['tunnels'][0]['public_url']
        # return redirect(f'{ngrok_url}/interface/cashier')
        # return redirect('https://e614-61-218-122-234.ngrok-free.app/interface/cashier')
        return redirect('http://127.0.0.1:8000/interface/cashier')

    return render(request, 'interface\\camera.html')

# 收銀區頁面
def cashier(request):
    file_path = './static/file/rfid.txt'
    # 檢查檔案是否存在
    if os.path.exists(file_path):
        # 打開檔案 讀取內容
        with open('./static/file/rfid.txt', 'r') as file:
            rfid_data = file.read()
        try:
            buyer = user.objects.get(user_RFID=rfid_data)
            # 如果成功取得 user 物件，這裡執行存在時的動作
            print("in")
            writeDB()
        except ObjectDoesNotExist:
            # 如果找不到對應的 user 物件，這裡執行不存在時的動作
            flask_url = "https://0a98-60-250-225-149.ngrok-free.app/newRecord"
            # print(type(uid_value))
            response = requests.post(flask_url, data={'new_record':"1"})
            if response.status_code == 200:
                print('success')
            else:
                print('failed', response.status_code)
    else:
        pass


    # 如果體積檔案根本不在，就跳到negative.html
    if not os.path.exists('./static/file/volume.txt'):
        return render(request, 'interface\\negative.html')
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
    cost = int(round(read_volume[0], 0))
    weight = round(read_volume[1], 3)
    calories = round(read_volume[2], 3)

    # 如果體積出現負值，就跳到negative.html
    if cost<0 or weight<0 or calories<0:
        return render(request, 'interface\\negative.html')
    
    context = {'cost': cost, 'weight': ("%.03f" % weight), 'calories': ("%.03f" % calories)}
    return render(request, 'interface\cashier.html',context)

# 出現負值的頁面
def negative(request):
    negativeDelete()
    return render(request, 'interface\\negative.html')

# from django.views.decorators.http import require_GET
# @require_GET
def getUserBool(request):
    reading_flag = True
    while reading_flag:
        # print(request.GET)
        userBool = request.GET.get('add_database')
        # print(request.GET)
        # print(type(userBool))
        if userBool == '1':
            print('userBool: ', userBool)
            print(type(userBool))
            # return render(request, 'interface\camera.html')
            # return redirect('http://127.0.0.1:8000/interface/camera')
            reading_flag = False
            print('userBool: ', userBool)
            print(type(userBool))
            return JsonResponse({'Thanks': "1"})




# 顯示圖片(不重要，紀念用而已)
# def img(request):
#     # 讀取圖片
#     img = cv2.imread('./media/interface/Totoro.png')
#     img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
#     _, image_encoded = cv2.imencode('.jpg', img) 
#     return HttpResponse(image_encoded.tostring(), content_type='image/jpeg') 

