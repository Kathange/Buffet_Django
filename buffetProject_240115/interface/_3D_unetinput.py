import subprocess
import json
from .models import *

def unetPredict(finfo):
    script_path = "unet_web/L515andPredict.py"
    try:
        print("Start subprocess")
        child_process = subprocess.Popen(["python", script_path],
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         text=True)

        # data = [[1, 2, 3], [4, 5, 6]]
        input_data = json.dumps(finfo)
        # input_bytes = input_data.encode()

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


def doing():
    finfo = readDB()
    print(finfo)
    unetPredict(finfo)

    finfo.clear()


