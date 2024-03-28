import os
from django.http import JsonResponse

def delete(request):
    if request.method == 'GET':
        # 如果 辨識照片 存在，就刪掉它
        image_path = './static/image/blend_img.png'
        if os.path.exists(image_path):
            os.remove(image_path)

        # 如果 donut_chart 存在，就刪掉它
        image_path = './static/image/donut_chart_seller.png'
        if os.path.exists(image_path):
            os.remove(image_path)

        # 如果 table 存在，就刪掉它
        image_path = './static/image/sheet_img.png'
        if os.path.exists(image_path):
            os.remove(image_path)

        # 如果 circle 存在，就刪掉它
        image_path = './static/image/circle.png'
        if os.path.exists(image_path):
            os.remove(image_path)

        # 如果 screen_shot 存在，就刪掉它
        image_path = './static/image/screenShot.jpg'
        if os.path.exists(image_path):
            os.remove(image_path)


        # 如果 merge_data.txt 存在，就刪掉它
        file_path = './static/file/merged_data.txt'
        if os.path.exists(file_path):
            os.remove(file_path)

        # 如果 volume.txt 存在，就刪掉它
        file_path = './static/file/volume.txt'
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # 如果 forUnet.csv 存在，就刪掉它
        file_path = './static/file/forUnet.csv'
        if os.path.exists(file_path):
            os.remove(file_path)

        # 如果 rfid.txt 存在，就刪掉它
        file_path = './static/file/rfid.txt'
        if os.path.exists(file_path):
            os.remove(file_path)
        print("delete in")

        return JsonResponse({'status': 'success'})



def negativeDelete():
    # 如果 辨識照片 存在，就刪掉它
    image_path = './static/image/blend_img.png'
    if os.path.exists(image_path):
        os.remove(image_path)

    # 如果 donut_chart 存在，就刪掉它
    image_path = './static/image/donut_chart_seller.png'
    if os.path.exists(image_path):
        os.remove(image_path)

    # 如果 table 存在，就刪掉它
    image_path = './static/image/sheet_img.png'
    if os.path.exists(image_path):
        os.remove(image_path)

    # 如果 circle 存在，就刪掉它
    image_path = './static/image/circle.png'
    if os.path.exists(image_path):
        os.remove(image_path)

    # 如果 screen_shot 存在，就刪掉它
    image_path = './static/image/screenShot.jpg'
    if os.path.exists(image_path):
        os.remove(image_path)


    # 如果 merge_data.txt 存在，就刪掉它
    file_path = './static/file/merged_data.txt'
    if os.path.exists(file_path):
        os.remove(file_path)

    # 如果 volume.txt 存在，就刪掉它
    file_path = './static/file/volume.txt'
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # 如果 forUnet.csv 存在，就刪掉它
    file_path = './static/file/forUnet.csv'
    if os.path.exists(file_path):
        os.remove(file_path)

    return None
