from django.shortcuts import render
from .models import *
from .camera import FoodVedioCamera, WasteVedioCamera
from django.http.response import StreamingHttpResponse
import qrcode
import os

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

def WasteVedioFeed(request):
    return StreamingHttpResponse(gen(WasteVedioCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')




# 創建網頁
def camera(request):
    return render(request, 'interface\camera.html')

def analysis(request):
    return render(request, 'interface\\analysis.html')

def cashier(request):
    # 建立qrcode
    img = qrcode.make('http://127.0.0.1:8000/interface/nutritionInfo')
    img.save("./static/image/qrcode.png")
    
    #從資料庫拿取資料
    user_list = user.objects.all()  # 把所有資料庫的資料取出
    context = {'user_list': user_list}
    return render(request, 'interface\cashier.html',context)

def nutritionInfo(request):
    # os.remove(os.path.join("./static/image", "qrcode.png"))
    return render(request, 'interface\\nutritionInfo.html')

def loginData(request):
    test_data = ['wafer_pie', 'oreo', 'yuki', 'snow_cracker', 'rice_cracker', 'rye_biscuit']
    test_data_weight = [21*14/29, 27.6*9/27, 18.7*8/16, 38*5/24, 30*14/124, 30*3/11]
    test_data_calorie = [14/29*114, 9/27*135, 8/16*95.7, 5/24*189, 14/124*143, 3/11*121.3]
    test_data_protein = [14/29*2.3, 9/27*1.3, 8/16*1.2, 5/24*1.7, 14/124*1.3, 3/11*2.2]
    test_data_carbohydrate = [14/29*11.2, 9/27*19.7, 8/16*12.1, 5/24*27.6, 14/124*22.4, 3/11*22.2]
    test_data_fat = [14/29*6.7, 9/27*5.7, 8/16*4.7, 5/24*8.0, 14/124*5.4, 3/11*2.9]
    # test_data_user_account = ['chocolate', 'redpanda', 'vicky', 'wxn', 'YP']
    # test_data_user_password = ['0101', '0924', '1010', '1229', '0918']
    # test_data_Iscustomer = [False, False, False, False, True]

    # for i in range(len(test_data_user_account)):
    #     user.objects.create(account = test_data_user_account[i], password = test_data_user_password[i], customer = test_data_Iscustomer[i])

    # for i in range(len(test_data)):
    #     food_code.objects.create(name = test_data[i])
    #     provide_food.objects.create(name = test_data[i])
    #     food_info.objects.create(weight = test_data_weight[i], calorie = test_data_calorie[i], protein = test_data_protein[i], carbohydrate = test_data_carbohydrate[i], fat = test_data_fat[i])
    return render(request, 'interface\loginData.html')

def buyerData(request):
    return render(request, 'interface\\buyerData.html')

def sellerData(request):
    return render(request, 'interface\sellerData.html')

def logUpData(request):
    return render(request, 'interface\logUpData.html')

def changePW(request):
    return render(request, 'interface\changePW.html')

def about(request):
    return render(request, 'interface\\about.html')


# 顯示圖片(不重要，紀念用而已)
# def img(request):
#     # 讀取圖片
#     img = cv2.imread('./media/interface/Totoro.png')
#     img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
#     _, image_encoded = cv2.imencode('.jpg', img) 
#     return HttpResponse(image_encoded.tostring(), content_type='image/jpeg') 

