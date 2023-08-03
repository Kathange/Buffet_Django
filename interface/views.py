from django.shortcuts import render
from .models import BuffetCalories
# import cv2

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
    # 建立 Dict對應到 BuffetCalories的資料 ({在html中所使用的名稱 : buyer這個class中宣告的變數名稱})
    context = {'calories' : calories}


    # 因為'\b'為跳脫字元，所以要'\'存在，要再加一個'\'跳脫
    return render(request, 'interface\\buyer.html', context)


