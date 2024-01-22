#----------------------------------------------------#
#   将单张图片预测、摄像头检测和FPS测试功能
#   整合到了一个py文件中，通过指定mode进行模式的修改。
#----------------------------------------------------#
# import time

# import pyrealsense2 as rs
# import cv2 as cv    
import numpy as np
from PIL import Image

from unet import Unet_ONNX, Unet

import csv

# import tkinter as tk
# from PIL import ImageTk

import sys
import json

import os


# if __name__ == "__main__":
#     try:
#         # Read from stdin
#         fInfo = sys.stdin.read()
#         # print("Received input in the subprocess:")
#         # print(fInfo)
#         # print(type(fInfo))

#         # Parse the JSON input
#         try:
#             input_list = json.loads(fInfo)
#         except json.JSONDecodeError as e:
#             print(f"Error decoding JSON: {e}")
#             sys.exit(1)

#         # # Process the 2D list (here, just printing)
#         # print("Received 2D list in the subprocess:")
#         # print(input_list)
#         # print(type(input_list))  # Fix: Print the correct variable type

#     except Exception as e:
#         print(f"Error in subprocess: {e}")
#         sys.exit(1)

#     sys.exit(0)




if __name__ == "__main__":
    try:
        # Read from stdin
        fInfo = sys.stdin.read()
        print("Received input in the subprocess:")
        print(fInfo)
        print(type(fInfo))

        # Parse the JSON input
        try:
            input_list = json.loads(fInfo)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            sys.exit(1)

        # Process the 2D list (here, just printing)
        print("Received 2D list in the subprocess:")
        print(input_list)
        print(type(input_list))  # Fix: Print the correct variable type
            


        # predict setting
        count           = True
        # name_classes    = ['_background_','wafer_pie', 'oreo', 'yuki', 'snow_cracker', 'rice_cracker', 'rye_biscuit']
        # classes_num     = 7
        name_classes    = ['_background_']
        classes_num     = 1
        for item in input_list:
            name_classes.append(item[0])
            classes_num += 1
        
        
        # File name to read the data
        file_name = './static/file/forUnet.csv'

        after_height = 0
        after_width = 0
        after_real_height_map = []
        with open(file_name, mode="r") as file:
            reader = csv.reader(file)
            cnt = 0
            for row in reader:
                if len(row) == 2:
                    if cnt == 0:
                        after_height =int(row[1])
                    elif cnt == 1:
                        after_width =int(row[1])
                    cnt += 1
                elif len(row) > 0 and row[0] == 'real_height_map':
                    after_real_height_map = [list(map(float, r)) for r in reader]
                else:
                    pass

        # 放進模型切割
        unet = Unet()
        # img = "unet_web/tmp/color_tmp.jpg"
        img = "unet_web/tmp/screenShot.jpg"
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')

        else:
            r_image = unet.detect_image(image, count=count, name_classes=name_classes)
            # r_image.show()
            # r_image.save("unet_web/result/blend_img.png", format="PNG")
            r_image.save("static/image/blend_img.png", format="PNG")

        #mask灰度圖
        mask = Image.open("unet_web/tmp/total_mask.png").convert('L')
        mask_width, mask_height = mask.size
        # print("mask_width, mask_height",(mask_width, mask_height))
        

        #由灰度圖來辨別食物的位置
        total_height = np.zeros(classes_num, dtype=float)
        target_imgs = [np.zeros((after_height, after_width, 3), dtype=np.uint8) for _ in range(classes_num)]
        for y in range(mask_width):
                    for x in range(mask_height):
                        pixel_value = mask.getpixel((y,x))
                        (target_imgs[pixel_value])[x][y] = (0, 0, 255)
                        #if (real_height_map[x][y] > critical_height_value):
                        total_height[pixel_value] += after_real_height_map[x][y]
        weight_a = -0.00005
        weight_b = 0.3504
        weight_c = 1.8748
        volume = []
        for i in range(1,classes_num):
            # volume = total_height[i] * total_height[i]*weight_a +total_height[i]*weight_b+weight_c
            volume.append(total_height[i] * total_height[i]*weight_a +total_height[i]*weight_b+weight_c)





        # 計算食物詳細熱量與價錢
        # class_name = ["wafer_pie", "oreo", "yuki" , "snow_craker", "rice_craker", "rye_biscuit"]
        # del name_classes[0]

        # food_info =[
        #     ['食物種類',	'重量(g)',	'熱量(Cal)',	'蛋白質(g)',	'碳水化合物(g)', '脂防(g)','價格(元))'],
        #     ['新貴派',   10.138,  55.034,  1.11,    5.407,  3.234 , 4.655],
        #     ['oreo',        9.2,	  45,	   0.433,	6.567,	1.9, 3.296],
        #     ['yuki',        9.35,	  47.85,   0.6,	    6.05,	2.35, 3.563],
        #     ['雪餅', 7.917,	  39.375,  0.354,	5.75,	1.667, 2.958],
        #     ['旺旺仙貝', 3.387,	  16.145,  0.147,	2.529,	0.61, 1.048],
        #     ['黑麥口糧', 8.182,	  33.082,  0.6,	    6.055,	0.791, 1.091]
        # ]


        for i in range(6):
            if float(volume[i]) == 1.8748:
                volume[i] = 0
            elif i == 0:
                volume[i] = round(volume[i]/18.71, 3)
            elif i == 1:
                volume[i] = round(volume[i]/19.33, 3)
            elif i == 2:
                volume[i] = round(volume[i]/20.19, 3)
            elif i == 4:
                volume[i] = round(volume[i]/8.89, 3)
            elif i == 3:
                volume[i] = round(volume[i]/19.32, 3)
            elif i == 5:
                volume[i] = round(volume[i]/25.59, 3)
            else:
                pass


        for i in range(6):
            for j in range(6):
                input_list[i+1][j+1] = round(float(volume[i])*float(input_list[i+1][j+1]), 2)

        total_price = 0
        total_weight = 0
        total_cal = 0
        for i in range(6):
            total_price += input_list[i+1][6] 
            total_weight += input_list[i+1][1]
            total_cal += input_list[i+1][2]
        show_on_cashier = [total_price, total_weight, total_cal]

        # print("show_on_cashier",show_on_cashier)
        # Save merged data to a text file
        with open('./static/file/volume.txt', 'w') as file:
            for item in show_on_cashier:
                if isinstance(item, list):
                    file.write(','.join(map(str, item)) + '\n')
                else:
                    file.write(str(item) + '\n')


        # show = [[0 for j in range(5)] for i in range(6)]
        # for j in range(6):
        #     for i in range(5):
        #         show[j][i] = input_list[j+1][i+1]

        # print("show", show)
        # Save merged data to a text file
        # with open('./static/file/merged_data.txt', 'w') as file:
        #     for item in show:
        #         file.write(','.join(map(str, item)) + '\n')

        file_path = './static/file/rfid.txt'
        # 檢查檔案是否存在 -- 如果不是會員，就不用詳細營養資訊，反正他也看不到
        if os.path.exists(file_path):
            with open('merged_data.txt', 'w') as file:
                for item in input_list:
                    # 使用过滤器保留只是数字的部分
                    numeric_values = [str(value) for value in item if isinstance(value, (int, float))]
                    file.write(','.join(numeric_values) + '\n')
        else:
            pass

    except Exception as e:
        print(f"Error in subprocess: {e}")
        sys.exit(1)

    sys.exit(0)
