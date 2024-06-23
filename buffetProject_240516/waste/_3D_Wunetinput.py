import subprocess
import json
from interface.models import *

def unetPredict(finfo, bone_food_names):
    script_path = "unet_web/L515andPredictWaste.py"
    try:
        print("Start subprocess")
        child_process = subprocess.Popen(["python", script_path],
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         text=True)

        # data = [[1, 2, 3], [4, 5, 6]]
        input_data = json.dumps({
            "finfo": finfo,
            "bone_food_names": bone_food_names
        })

        # Send input data to the subprocess
        output, error = child_process.communicate(input=input_data)

        print("Subprocess output:")
        print(output)
        if error:
            print("Error: ", error)
    except Exception as e:
        print(f"Subprocess error: {e}")

    finally:
        # Close standard input, notifying the subprocess that no more data will be sent
        child_process.stdin.close()
        # # Wait for the subprocess to complete
        # child_process.wait()
        # Terminate the subprocess
        child_process.terminate()
    print("Subprocess completed")
    return None

def readDB():
    finfo = []
    # 查询拥有 provide_food 的 food_code
    foods_with_provide_food = food_code.objects.filter(fk_prvideFood_name__isnull=False)
    # 打印结果
    # for food in foods_with_provide_food:
        # print(f"Food ID: {food.food_id}, Name: {food.name}")

    # 遍历这些 food_code 对象，然后查询 food_info 中与之关联的数据
    for food_code_obj in foods_with_provide_food:
        # 查询 food_info 中与当前 food_code 相关联的数据
        food_info_objects = food_info.objects.filter(food_id__food_id=food_code_obj.food_id)
        # 打印结果
        for food_info_obj in food_info_objects:
            finfo.append([food_code_obj.name, float(food_info_obj.weight), float(food_info_obj.calorie), float(food_info_obj.protein), float(food_info_obj.carbohydrate), float(food_info_obj.fat), float(food_info_obj.cost)])
            # print(f"Food ID: {food_info_obj.food_id.food_id}, Weight: {food_info_obj.weight}, Calorie: {food_info_obj.calorie}")

    # print(finfo)
    return finfo

def getBoneFoodNames():
    # 读取RFID
    with open('./static/file/rfid.txt', 'r') as file:
        rfid_data = file.read()
    # 拿取RFID的主人的id
    buyer = user.objects.get(user_RFID=rfid_data)
    # 获取该用户的最后一个记录
    record_ori = record.objects.filter(user_line=buyer).last()
    # 获取与 record 相关的所有 detail_record
    detail_record_ori = detail_record.objects.filter(record_id=record_ori).values_list('food_id', flat=True)
    # 过滤food_info中is_bone为True且food_id在detail_record_ori的记录
    bone_foods = food_info.objects.filter(is_bone=True, food_id__in=detail_record_ori).values_list('food_id', flat=True)
    # 从 food_code 中获取对应的名称
    food_names = food_code.objects.filter(food_id__in=bone_foods).values_list('name', flat=True)
    # 转换为字符串组成的list
    food_names_list = list(food_names)

    return food_names_list



def doing():
    finfo = readDB()
    bone_food_names = getBoneFoodNames()

    print(finfo)
    print(bone_food_names)

    unetPredict(finfo, bone_food_names)

    finfo.clear()
    bone_food_names.clear()


