from django.shortcuts import render, redirect
from .models import *
from django.http.response import StreamingHttpResponse
# import qrcode
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login
# from django.conf import settings
from django.http import JsonResponse
import subprocess
import time
import ast
import json
import os
import requests

from ._3D_camera import FoodVedioCamera
from ._3D_getDB import getDBAllData
from ._3D_writeDB import writeDB
from ._3D_unetinput import doing


# matplotlib.use('Agg')

# Create your views here.
# def buyer(request):
#     buffet_list = BuffetCalories.objects.all()  # 把所有資料庫的資料取出來

#     # 以下3種方法會 print 出一樣的東西 (都會print出database所有的值)
#     # 法一
#     # for food in buffet_list:
#     #     print(food)
#     # 法二
#     # print(buffet_list)
#     # 法三
#     # for food in buffet_list:
#     #     print(f"{food.food_name} {food.food_volume} {food.food_calories}")
    
#     # 知道如何拿到database資料之後，舉個例
#     # 目標：算出總熱量
#     calories = 0
#     for food in buffet_list:
#         # food.food_name == 當前偵測到食物的名字
#         if food.food_name == 'rice':
#             calories += food.food_calories
    
#     # 因為'\b'為跳脫字元，所以要'\'存在，要再加一個'\'跳脫
#     # {'calories' : calories}：建立 Dict對應到 BuffetCalories的資料 ({在buyer.html中所使用的名稱 : buyer這個class中宣告的變數名稱})
#     return render(request, 'interface\\buyer.html', {'calories' : calories})

# # 廚餘區
# def unpopular(request):
#     unpopular_list = UnpopularFoods.objects.all()
#     print(unpopular_list)
#     return render(request, 'home.html', {'unpopular' : unpopular_list})

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


# 用subprocess跑體積和unet程式
name_classes    = ['wafer_pie', 'oreo', 'yuki', 'snow_cracker', 'rice_cracker', 'rye_biscuit']
ch_name_classes = ['新貴派','oreo','yuki','雪餅','旺旺仙貝','黑麥口糧']

def joinMember(request):
    return render(request, 'interface\\joinMember.html')

def camera(request):
    getDBAllData()
    if request.method == 'POST':
        doing()
        # unetPredict(request)
        # return redirect('https://ae83-2402-7500-569-2d92-3132-620f-ac8a-77c1.ngrok-free.app/interface/cashier')
        # return render(request, 'interface\\cashier.html')
        return redirect('http://127.0.0.1:8080/interface/cashier')
    return render(request, 'interface\\camera.html')

def cashier(request):
    file_path = './static/file/rfid.txt'
    # 檢查檔案是否存在
    if os.path.exists(file_path):
        print("in")
        writeDB()

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
    show_to_cashier = read_volume
    cost = int(round(show_to_cashier[0], 0))
    weight = round(show_to_cashier[1], 3)
    calories = round(show_to_cashier[2], 3)
    
    # context = {'weight': weight, 'calories': calories, 'cost': round(cost)}
    context = {'cost': cost, 'weight': ("%.03f" % weight), 'calories': ("%.03f" % calories)}
    return render(request, 'interface\cashier.html',context)

def nutritionInfo(request):
    # os.remove(os.path.join("./static/image", "qrcode.png"))

    #從資料庫拿取資料
    detail = detail_record.objects.all()  # 把所有資料庫的資料取出
    total = record.objects.all()
    
    # queryset1 = record.objects.filter(eat_date='2023-10-04')
    # queryset2 = detail_record.objects.filter(record_id=queryset1)
    # print(queryset1)
    # print(queryset2)

    # # 建立環圈圖
    # matplotlib.rc('font', family='Microsoft JhengHei')
    # # Data，這邊到時候是叫資料庫資料
    # # labels = ['A', 'B', 'C', 'D']
    # # sizes = [15, 30, 45, 10]
    # labels = ['碳水化合物','蛋白質','脂質']
    # # labels = ['carbohydrate','protein','fat']
    # sizes = [32.357, 3.245, 10.552]
    # # colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    # colors = ['gold', 'yellowgreen', 'lightcoral']
    # explode = (0.05, 0.05, 0.05)  # To create a gap and make it a donut
    
    # # print(queryset1.total_pro)
    # # sizes.append(queryset1.total_pro)
    # # sizes.append(queryset1.total_carbo)
    # # sizes.append(queryset1.total_fat)
    # # print(sizes)
    # # # sizes.append(queryset1.get(record_id=rec1.id).total_pro)
    # # # sizes.append(queryset1.get(record_id=rec1.id).total_carbo)
    # # # sizes.append(queryset1.get(record_id=rec1.id).total_fat)

    # # 創建環圈圖
    # _, texts, _ = plt.pie(sizes, 
    #                     explode=explode, 
    #                     labels=labels, 
    #                     colors=colors, 
    #                     autopct='%1.1f%%', 
    #                     pctdistance=0.7, 
    #                     radius=1.5, 
    #                     textprops={'color':'w','weight':'bold','size':10})
    # # 隱藏外側的標籤
    # for text in texts:
    #     text.set_visible(False)
    # # 把圓餅圖中間加上一個圓，就可變成環圈圖
    # circle = plt.Circle((0, 0), 0.70, fc='#eaeaea')
    # plt.gca().add_artist(circle)
    # # 加上圖例
    # # plt.legend(labels, loc="center right", bbox_to_anchor=(1.0, 0.0))
    # plt.legend(labels, loc="center right")
    # # 確保圖表繪製為具有相等長寬比的圓形
    # plt.axis('equal')
    # # 儲存圖片
    # plt.savefig('./static/image/donut_chart.png', transparent=True)

    context = {'detail': detail, 'total': total}
    return render(request, 'interface\\nutritionInfo.html',context)

def seller_info(request):
    # Read merged data from the text file
    read_merged_list = []
    # Read data from 'merged_data.txt'
    with open('./static/file/merged_data.txt', 'r') as file:
        read_merged_list = [list(map(float, line.strip().split(','))) for line in file]
    print(read_merged_list)

    show = []
    total = [0.0, 0.0, 0.0, 0.0, 0.0]
    for i in range(len(name_classes)):
        if read_merged_list[i][0] == 0:
            continue
        show.append([name_classes[i]] + read_merged_list[i])
        for j in range(len(read_merged_list[i])):
            total[j] += read_merged_list[i][j]
            total[j] = round(total[j], 3)
    print(total)
    show.append(['Total'] + total)
    # read_merged_list.clear()


    # # 建立環圈圖
    # matplotlib.rc('font', family='Microsoft JhengHei')
    # labels = ['Protein','Carbohydrate','Fat']
    # sizes = total[-3:]
    # print(sizes)
    # colors = ['gold', 'yellowgreen', 'lightcoral']
    # explode = (0.05, 0.05, 0.05)
    # # 創建環圈圖
    # _, texts, _ = plt.pie(sizes, 
    #                     explode=explode, 
    #                     labels=labels, 
    #                     colors=colors, 
    #                     autopct='%1.1f%%', 
    #                     pctdistance=0.7, 
    #                     radius=1.5, 
    #                     textprops={'color':'w','weight':'bold','size':10})
    # # 隱藏外側的標籤
    # for text in texts:
    #     text.set_visible(False)
    # # 把圓餅圖中間加上一個圓，就可變成環圈圖
    # circle = plt.Circle((0, 0), 0.70, fc='#eaeaea')
    # plt.gca().add_artist(circle)
    # # 加上圖例
    # plt.legend(labels, loc="center right")
    # # 確保圖表繪製為具有相等長寬比的圓形
    # plt.axis('equal')
    # # 儲存圖片
    # plt.savefig('./static/image/donut_chart_seller.png', transparent=True)
    # # 儲存到緩衝區
    # buffer = BytesIO()
    # plt.savefig(buffer, format='png', bbox_inches='tight')
    # buffer.seek(0)

    # # 替換成您的照片檔案路徑和 Imgur Token
    # imgur_token = '412b87ea68ecab734b84985d38a425f5e56623e1'
    # # 上傳照片並獲取 Imgur 照片的連結
    # imgur_link = upload_image(buffer, imgur_token)
    # if imgur_link:
    #     print(f'Imgur 照片的連結為：{imgur_link}')

    # total.clear()
    context = {'show': show}
    return render(request, 'interface\\seller_info.html', context)


def about(request):
    # doing()
    return render(request, 'interface\\about.html')

def buyerData(request):
    #從資料庫拿取資料
    records = record.objects.all()  # 把所有資料庫的資料取出
    
    # date_count = []
    # for rec in records:
    #     date_count.append(rec.eat_date)
    
    # my_user = request.user
    # #If you want to know if the user is logged in
    # is_user_logged = my_user.is_authenticated
    context = {'records': records}
    return render(request, 'interface\\buyerData.html',context)

def sellerData(request):
    #從資料庫拿取資料
    records = record.objects.all().order_by('eat_date').values()  # 把所有資料庫的資料取出
    context = {'records': records}
    return render(request, 'interface\sellerData.html',context)

def loginData(request):
    if request.method == "GET":
        return render(request, 'interface\\loginData.html')
    if request.method == "POST":
        account = request.POST.get('account')
        # username = request.POST.get('account')
        password = request.POST.get('password')
        
        
        # user = authenticate(request, account = account, password = password)
        # if user is not None:
        #     if user.is_active:
        #         login(request, user)
        # else:
        #     error_msg = "account dose not exist"
        #     return render(request, 'interface\\loginData.html', {'error_msg': error_msg})
        

        # 正確段落
        try:
            user_detect = user.objects.get(account = account)
        # if user_detect:
            if password == user_detect.password:
                if user_detect.customer == True:
                    # user = authenticate(request, username=account, password=password)
                    # login(request, user_detect)
                    return redirect('http://127.0.0.1:8000/interface/buyerData')
                else:
                    # login(request, user_detect)
                    return redirect('http://127.0.0.1:8000/interface/sellerData')
            else :
                error_msg = "password wrong"
                return render(request, 'interface\\loginData.html', {'error_msg': error_msg})
            # user_login = authenticate(request, account = account, password = password)
            # user_detect = authenticate(request, username = username, password = password)
        except:
        # else:
            error_msg = "account dose not exist"
            return render(request, 'interface\\loginData.html', {'error_msg': error_msg})
          
            # if password != user_detect.password:
                # if user_detect.customer == True:
                # user_login = authenticate(request, account = account, password = password)
            # if user_login is not None:
                # login(request, user_detect)
            # if user_detect.customer == True:
                # if user_detect is not None:
                    # user_login = authenticate(request, account = account, password = password)
                    # return redirect('http://127.0.0.1:8000/interface/buyerData')
                # else:
                    # return redirect('http://127.0.0.1:8000/interface/sellerData')
            # else:
            #     error_msg = "password error"
                # return render(request, 'interface\\loginData.html', {"error_msg": error_msg})
        # except:
        #     error_msg = "account does not exist"
        #     return render(request, 'interface\\loginData.html', {'error_msg': error_msg})

def logUpData(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        try:
            user_account = user.objects.get(account=account)
            if user_account:
                error_msg="account is exist"
                return render(request, 'interface\\logUpData.html', {'error_msg': error_msg})
        except:
            if password != repassword:
                error_msg = "password inconsistent"
                return render(request, 'interface\\logUpData.html', {'error_msg': error_msg})
            else:
                register = user()
                register.account = account
                register.password = password
                register.save()
                return redirect('http://127.0.0.1:8000/interface/loginData')
    else:
        return render(request, 'interface\\logUpData.html')

@login_required(login_url = 'http://127.0.0.1:8000/interface/loginData')
def changePW(request):
    # if request.method == "POST":
    #     user_info = user.objects.get(account=request.account)
    #     orgin_password = request.POST.get('origin_password')
    #     new_password = request.POST.get('new_password')
    #     new_repassword = request.POST.get('new_repassword')
    #     try:
    #         user_detect = user.objects.get(account = account)
    #         if password == user_detect.password:
    #             if user_detect.customer == True:
    #                 return redirect('http://127.0.0.1:8000/interface/buyerData')
    #             else:
    #                 return redirect('http://127.0.0.1:8000/interface/sellerData')
    #         else:
    #             error_msg = "password error"
    #             return render(request, 'interface\\loginData.html', {"error_msg": error_msg})
    #     except:
    #         error_msg = "account does not exist"
    #         return render(request, 'interface\\loginData.html', {'error_msg': error_msg})
    return render(request, 'interface\changePW.html')



# 顯示圖片(不重要，紀念用而已)
# def img(request):
#     # 讀取圖片
#     img = cv2.imread('./media/interface/Totoro.png')
#     img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
#     _, image_encoded = cv2.imencode('.jpg', img) 
#     return HttpResponse(image_encoded.tostring(), content_type='image/jpeg') 





def trigger_condition(request):
    variable_to_send = 'Hello'
    flask_url = "https://9571-36-231-202-57.ngrok-free.app/endpoint"
    response = requests.post(flask_url, data={'variable_name':variable_to_send})

    if response.status_code == 200:
        print('success')
    else:
        print('failed', response.status_code)
    # return HttpResponse('Response from Django')
    return render(request, 'interface\\trigger_condition.html')


def getUserBool(request):
    reading_flag = True
    while reading_flag:
        userBool = request.POST.get('add_database')
        if userBool == '1':
            reading_flag = False
            print('userBool: ', userBool)
            return JsonResponse({'Thanks': userBool})
    
