"""

此為拿取資料庫中所有資料

"""


from .models import *
from django.db import connection

def getDBAllData():
    # # 拿取 interface_food_code
    # foodCode = food_code.objects.all()
    # print("food_code:")
    # for food in foodCode:
    #     print(f"Food ID: {food.food_id}, Name: {food.name}")
    # print()

    # # 拿取 interface_provide_food
    # provideFood = provide_food.objects.all()
    # print("provide_food:")
    # for food in provideFood:
    #     print(f"Name: {food.name}")
    # print()
    
    # # 拿取 interface_food_info
    # foodInfo = food_info.objects.all()
    # print("food_info:")
    # for food in foodInfo:
    #     print(f"Food ID: {food.food_id}, Weight: {food.weight}, Calorie: {food.calorie}, Protein: {food.protein}, Carbo: {food.carbohydrate}, Fat: {food.fat}, Cost: {food.cost}")
    # print()

    # 拿取 interface_user
    # User = user.objects.all()
    # print("user:")
    # for food in User:
    #     print(f"User ID: {food.user_id}, User_RFID: {food.user_RFID}, User_Line: {food.user_line}")
    # print()

    # # 拿取 interface_record
    # Record = record.objects.all()
    # print("record:")
    # for food in Record:
    #     print(f"Record ID: {food.record_id}, User ID: {food.user_id}, Eat Date: {food.eat_date}, Eat Time: {food.eat_time}, Total Weight: {food.total_weight}, Total Calorie: {food.total_cal}, Total Protein: {food.total_pro}, Total Carbo: {food.total_carbo}, Total Fat: {food.total_fat}, Cost: {food.cost}")
    # print()

    # # 拿取 interface_detail_record
    # detailRecord = detail_record.objects.all()
    # print("detail_record:")
    # for food in detailRecord:
    #     print(f"Record ID: {food.record_id}, Food ID: {food.food_id}, Weight: {food.weight}, Calorie: {food.calorie}, Protein: {food.protein}, Carbo: {food.carbohydrate}, Fat: {food.fat}")
    # print()


    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM interface_food_code ORDER BY food_id;")
    #     foodCode = cursor.fetchall()
    # print(foodCode)
    # # for food in foodCode:
    # #     print(f"Food ID: {food[0]}, Name: {food[1]}")
    # # print()
    # # for food_id, name in foodCode:
    # #     print(f"Food ID: {food_id}, Name: {name}")
    # # print()

    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM interface_provide_food;")
    #     provideFood = cursor.fetchall()
    # print(provideFood)

    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM interface_food_info;")
    #     foodInfo = cursor.fetchall()
    # print(foodInfo)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM interface_user;")
        User = cursor.fetchall()
    print(User)

    

    # User = cursor.fetchall()
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM interface_record;")
    #     Record = cursor.fetchall()
    # print(Record)

    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM interface_detail_record;")
    #     detailRecord = cursor.fetchall()
    # print(detailRecord)

    return None


