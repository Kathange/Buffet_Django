from django.shortcuts import render
from .models import BuffetCalories, UnpopularFoods
from .camera import FoodVedioCamera, WasteVedioCamera
from django.http.response import StreamingHttpResponse
import qrcode
import os

# Create your views here.
def buyer(request):
    buffet_list = BuffetCalories.objects.all()  # 把所有資料庫的資料取出來

    # 以下3種方法會 print 出一樣的東西 (都會print出database所有的值)
    # 法一
    # for food in buffet_list:
    #     print(food)
    # 法二
    # print(buffet_list)
    # 法三
    # for food in buffet_list:
    #     print(f"{food.food_name} {food.food_volume} {food.food_calories}")
    

    # 知道如何拿到database資料之後，舉個例
    # 目標：算出總熱量
    calories = 0
    for food in buffet_list:
        # food.food_name == 當前偵測到食物的名字
        if food.food_name == 'rice':
            calories += food.food_calories
    

    # 因為'\b'為跳脫字元，所以要'\'存在，要再加一個'\'跳脫
    # {'calories' : calories}：建立 Dict對應到 BuffetCalories的資料 ({在buyer.html中所使用的名稱 : buyer這個class中宣告的變數名稱})
    return render(request, 'interface\\buyer.html', {'calories' : calories})

def unpopular(request):
    unpopular_list = UnpopularFoods.objects.all()
    print(unpopular_list)
    return render(request, 'home.html', {'unpopular' : unpopular_list})

# 設置 camera (要把模型放進去應該去camera.py寫)
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def FoodVedioFeed(request):
    return StreamingHttpResponse(gen(FoodVedioCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def WasteVedioFeed(request):
    return StreamingHttpResponse(gen(WasteVedioCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')





def cashier(request):
    # if request.method=='POST':
    #     data = request.POST['data']
    #     img = qrcode.make(data)
    #     img.save("./static/image/qrcode1.png")
    # else:
    #     pass
    img = qrcode.make('http://127.0.0.1:8000/interface/nutritionInfo')
    img.save("./static/image/qrcode.png")
    return render(request, 'interface\cashier.html')

def nutritionInfo(request):
    # os.remove(os.path.join("./static/image", "qrcode.png"))
    return render(request, 'interface\\nutritionInfo.html')

def loginData(request):
    return render(request, 'interface\loginData.html')

def buyerData(request):
    return render(request, 'interface\\buyerData.html')

def sellerData(request):
    return render(request, 'interface\sellerData.html')

def logUpData(request):
    return render(request, 'interface\logUpData.html')

def changePW(request):
    return render(request, 'interface\changePW.html')

# 顯示圖片(不重要，紀念用而已)
# def img(request):
#     # 讀取圖片
#     img = cv2.imread('./media/interface/Totoro.png')
#     img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
#     _, image_encoded = cv2.imencode('.jpg', img) 
#     return HttpResponse(image_encoded.tostring(), content_type='image/jpeg') 

