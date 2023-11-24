from django.shortcuts import render, redirect
from .models import *
################暫時借我用，不然會有bug
from .models import user, food_info, record, detail_record
################暫時借我用，不然會有bug
from .camera import FoodVedioCamera, WasteVedioCamera
from django.http.response import StreamingHttpResponse, HttpResponse, HttpResponseServerError
import qrcode
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
# from .L515andPredict import L515andPredict
import subprocess
# from django.db.models import Sum
from time import sleep
# from .unet import Unet
# from PIL import Image
# import numpy as np
# from .camera import FoodVedioCamera
# from .call_unet import __init__ as unet
import keyboard

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
    # result = subprocess.run(["python","//interface//unet_sample//L515andPredict.py"], capture_output=True, text=True)
    # script_output = result.stdout
    # print(script_output)
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # script_path = '.L515andPredict.py'
        # try:
        #     result = subprocess.run(['python', script_path], capture_output=True, text=True, check=True)
        #     return HttpResponse("success")
        
        # except subprocess.CalledProcessError as e:
        #     return HttpResponseServerError("error")
        # return flag
        
        

    
    # while True:
    #     frame = camera.get_frame()
    #     # # L515andPredict()
    #     yield(b'--frame\r\n'
    #           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# 連接攝影機(特定語法，應該，我是複製貼上)，gen(camera.py中的class)
def FoodVedioFeed(request):
    # if gen(FoodVedioCamera()) == 3:
        # return redirect('http://127.0.0.1:8000/interface/analysis')
    return StreamingHttpResponse(gen(FoodVedioCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def WasteVedioFeed(request):
    return StreamingHttpResponse(gen(WasteVedioCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

# 創建網頁
flag = True
def camera(request):
    # # analysis_generator = FoodVedioCamera()  # Create an instance of the class
    # # n = 0
    # if request.method == "POST":
    #     # Handle the POST request here
    #     clickcount = int(request.POST.get('clickcount', 0))
    #     # clickcount += 1
    #     if clickcount == 2:
    #         clickcount = 0
    #         print("haha")
    #         return render(request, 'interface\\analysis.html')
    #         # response = HttpResponse('success', content_type="text/plain")
    #         # return response
    #     else:
    #         if keyboard.is_pressed('s'):
    #             print("before unet")
    #             weight_food, flag = unet()
    #             print("after unet")
    #         # unet = Unet

    #         sleep(3)
    #         print("333")
    #             # return render(request, 'interface\\analysis.html')
    #         print("555")
    #         # weight_food, flag = unet()
    #         return redirect('http://127.0.0.1:8000/interface/cashier')

    # else:# analysis_content = analysis_generator.get_frame()  # Call the analysis method to get content
    #     print("444")
    #     return render(request, 'interface\\camera.html')
    if request.method == "POST":
        subprocess.call(["python", "C:/desktopBackup/CGU/Topics/Cafeteria/buffetProject_1102/unet_web/L515andPredict.py"])
        print("okok")
    return render(request, 'interface\\camera.html')


def analysis(request):
    print("111")
    sleep(3)
    print("3")
    return render(request, 'interface\\analysis.html')   # self bug
    # return render(request, "interface\cashier.html")   # self bug
    # return redirect('http://127.0.0.1:8000/interface/cashier')  # self bug

def cashier(request):
    # 建立qrcode
    img = qrcode.make('http://127.0.0.1:8000/interface/nutritionInfo')
    img.save("./static/image/qrcode.png")
    
    #從資料庫拿取資料
    foods = food_info.objects.all()  # 把所有資料庫的資料取出

    # 知道如何拿到database資料之後，舉個例
    # 目標：算出總熱量
    weight = 0
    calories = 0
    cost = 0
    for food in foods:
        # food.food_name == 當前偵測到食物的名字
        weight += food.weight
        calories += food.calorie
        cost += food.cost

    context = {'weight': weight, 'calories': calories, 'cost': round(cost)}
    return render(request, 'interface\cashier.html',context)

def nutritionInfo(request):
    # os.remove(os.path.join("./static/image", "qrcode.png"))

    #從資料庫拿取資料
    detail = detail_record.objects.all()  # 把所有資料庫的資料取出
    total = record.objects.all()
    
    queryset1 = record.objects.filter(eat_date='2023-10-04')
    # queryset2 = detail_record.objects.filter(record_id=queryset1)
    # print(queryset1)
    # print(queryset2)

    # 建立環圈圖
    # Data，這邊到時候是叫資料庫資料
    # labels = ['A', 'B', 'C', 'D']
    # sizes = [15, 30, 45, 10]
    # labels = ['碳水化合物','蛋白質','脂質']
    labels = ['carbohydrate','protein','fat']
    sizes = [32.357, 3.245, 10.552]
    # colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    colors = ['gold', 'yellowgreen', 'lightcoral']
    explode = (0.05, 0.05, 0.05)  # To create a gap and make it a donut
    
    # print(queryset1.total_pro)
    # sizes.append(queryset1.total_pro)
    # sizes.append(queryset1.total_carbo)
    # sizes.append(queryset1.total_fat)
    # print(sizes)
    # # sizes.append(queryset1.get(record_id=rec1.id).total_pro)
    # # sizes.append(queryset1.get(record_id=rec1.id).total_carbo)
    # # sizes.append(queryset1.get(record_id=rec1.id).total_fat)

    # 創建環圈圖
    _, texts, _ = plt.pie(sizes, 
                        explode=explode, 
                        labels=labels, 
                        colors=colors, 
                        autopct='%1.1f%%', 
                        pctdistance=0.7, 
                        radius=1.5, 
                        textprops={'color':'w','weight':'bold','size':10})
    # 隱藏外側的標籤
    for text in texts:
        text.set_visible(False)
    # 把圓餅圖中間加上一個圓，就可變成環圈圖
    circle = plt.Circle((0, 0), 0.70, fc='#eaeaea')
    plt.gca().add_artist(circle)
    # 加上圖例
    plt.legend(labels, loc="center right")
    # 確保圖表繪製為具有相等長寬比的圓形
    plt.axis('equal')
    # 儲存圖片
    plt.savefig('./static/image/donut_chart.png', transparent=True)

    

    context = {'detail': detail, 'total': total}
    return render(request, 'interface\\nutritionInfo.html',context)

def loginData(request):
    if request.method == "GET":
        return render(request, 'interface\\loginData.html')
    if request.method == "POST":
        account = request.POST.get('account')
        password = request.POST.get('password')
        try:
            user_detect = user.object.get(account = account)
            # user_detect = user.objects.get(account = account)
            if password == user_detect.password:
                if user_detect.customer == True:
                    user_login = authenticate(username = account, password = password)
                    login(request, user_login)
                    return redirect('http://127.0.0.1:8000/interface/buyerData')
                else:
                    return redirect('http://127.0.0.1:8000/interface/sellerData')
            else:
                error_msg = "password error"
                return render(request, 'interface\\loginData.html', {"error_msg": error_msg})
        except:
            error_msg = "account does not exist"
            return render(request, 'interface\\loginData.html', {'error_msg': error_msg})

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
    # records = record.objects.filter(category='eat_date')
    # records = record.objects.values('eat_date').annotate()
    # queryset = MyModel.objects.filter(some_field=some_value).order_by('-date_field')
    # c = record.objects.filter(records='2023-10-04').aggregate(sum(total_cal))
    # queryset = record.objects.filter(date1='eat_date').distinct()
    # print(queryset)
    # for dates in records:
    # print(records)

    # totalqs = records.annotate(day_weight=Sum('total_weight'))
    # print(totalqs)
    # totalqs = records.annotate(day_cost=Sum('cost'))
    # print(totalqs)

    # queryset = record.objects.filter(eat_date='2023-10-04')
    # # queryset = record.objects.annotate(total_value=Sum('amount'))
    # print(queryset)
    # queryset = queryset.annotate(day_weight=Sum('total_weight'))
    # print(queryset)
    # queryset = queryset.annotate(day_cost=Sum('cost'))
    # print(queryset)

    # date_list = []
    # for dates in records:
    #     date_list.append({'eat_date': dates['eat_date']})
    #     # date_list.append(dates.eat_date)
    # # for dates in records:
    # print(date_list)
    # # #     date_list.append(dates.eat_date)
    # # # print(date_list)
    # context = {'records': records}
    context = {'records': records}
    # # context = {'date_list', date_list}
    # # # for i in range(len(date_list)):
    # # #     if date_list[i] == 
    # # # context = {'date_list', date_list}
    # # print(date_list)
    return render(request, 'interface\sellerData.html',context)

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

def seller_info(request):
    return render(request, 'interface\\seller_info.html')


# 顯示圖片(不重要，紀念用而已)
# def img(request):
#     # 讀取圖片
#     img = cv2.imread('./media/interface/Totoro.png')
#     img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
#     _, image_encoded = cv2.imencode('.jpg', img) 
#     return HttpResponse(image_encoded.tostring(), content_type='image/jpeg') 
