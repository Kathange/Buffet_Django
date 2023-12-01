#----------------------------------------------------#
#   将单张图片预测、摄像头检测和FPS测试功能
#   整合到了一个py文件中，通过指定mode进行模式的修改。
#----------------------------------------------------#
import time

import pyrealsense2 as rs
import cv2 as cv    
import numpy as np
from PIL import Image

from unet import Unet_ONNX, Unet

import csv

import tkinter as tk
from PIL import ImageTk
# from interface.models import *

if __name__ == "__main__":
    # #predict setting
    count           = True
    name_classes    = ['_background_','wafer_pie', 'oreo', 'yuki', 'snow_cracker', 'rice_cracker', 'rye_biscuit']
    classes_num     = 7
    
    # critical_height_value = 0.003 #過濾空白處的值
    # # setting
    # pipeline = rs.pipeline()
    # config = rs.config()

    # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    # config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
    # config.enable_device('f0233004')

    # #對齊像素
    # align_to = rs.stream.color
    # align = rs.align(align_to)

    # # 啟動深度攝影機
    # profile = pipeline.start(config)

    # # 取得深度攝影機的sensor物件
    # depth_sensor = profile.get_device().first_depth_sensor()
    # depth_sensor.set_option(rs.option.visual_preset,5)


    # # 設定最大和最小深度值
    # colorizer = rs.colorizer()
    # colorizer.set_option(rs.option.visual_preset, 1) # 0=Dynamic, 1=Fixed, 2=Near, 3=Far
    # colorizer.set_option(rs.option.min_distance, 0.3)
    # colorizer.set_option(rs.option.max_distance, 2.7)
    # colorizer.set_option(rs.option.histogram_equalization_enabled, True)
    # #depth_sensor.set_option(rs.option.max_distance, max_distance)

    # #pipeline.start(config)
    # #影像
    # while True:
    #     #取得照片frame
    #     frame = pipeline.wait_for_frames()
    #     #把兩種frames對齊
    #     aligned_frames = align.process(frame)
    #     depth = aligned_frames.get_depth_frame()
    #     color = aligned_frames.get_color_frame()

    #     #轉換成圖片img
    #     depth_img = np.asanyarray(depth.get_data())
    #     color_img = np.asanyarray(color.get_data())
    
    #     # depth_cmap = cv.applyColorMap(cv.convertScaleAbs(depth_img, alpha = 0.25),cv.COLORMAP_JET)
    
    #     depth_colormap = np.asanyarray(colorizer.colorize(depth).get_data())
    #     #取得寬高
    #     width = depth.get_width()
    #     height = depth.get_height()


    #     #取得中心點
    #     # center = (int(width/2),int(height/2))
    #     #cv.circle(color_img, (center[0],center[1]), 4,(0,0,255),5)
    #     #cv.circle(depth_colormap, (center[0],center[1]), 4,(0,0,255),5)
    #     #距離
    #     # dist = depth.get_distance(center[0], center[1])
    #     #實際物品高度
    #     # real_height = camera_height - dist

        
        
        
        
    #     #顯示圖片
    #     cv.imshow('depth_colormap', depth_colormap)
    #     cv.imshow('rgb',color_img)
        
    #     #cv.imshow('depth',depth_cmap)
    #     #print(dist)
    #     #print(real_height, ' meter')
        
        
    #     #按Q就會拍照
    #     if cv.waitKey(1) == ord('q'):
    #         break

    # original_height_map = np.zeros((height,width))
    # for y in range(width):
    #         for x in range(height):
    #             #original_height_map[x][y] = 0.5
    #             original_height_map[x][y] = depth.get_distance(y, x)
                 




    # #攝影機高度
    
    # #影像
    # for times in range(1) :
    #     while True:
    #         #取得照片frame
    #         frame = pipeline.wait_for_frames()
    #         #把兩種frames對齊
    #         aligned_frames = align.process(frame)
    #         depth = aligned_frames.get_depth_frame()
    #         color = aligned_frames.get_color_frame()

    #         #轉換成圖片img
    #         depth_img = np.asanyarray(depth.get_data())
    #         color_img = np.asanyarray(color.get_data())
        
    #         # depth_cmap = cv.applyColorMap(cv.convertScaleAbs(depth_img, alpha = 0.25),cv.COLORMAP_JET)
        
    #         depth_colormap = np.asanyarray(colorizer.colorize(depth).get_data())
    #         #取得寬高
    #         width = depth.get_width()
    #         height = depth.get_height()


    #         #取得中心點
    #         # center = (int(width/2),int(height/2))
    #         #cv.circle(color_img, (center[0],center[1]), 4,(0,0,255),5)
    #         #cv.circle(depth_colormap, (center[0],center[1]), 4,(0,0,255),5)
    #         #距離
    #         # dist = depth.get_distance(center[0], center[1])
    #         #實際物品高度
    #         # real_height = camera_height - dist

            
            
            
            
    #         #顯示圖片
    #         cv.imshow('depth_colormap', depth_colormap)
    #         cv.imshow('rgb',color_img)
            
    #         #cv.imshow('depth',depth_cmap)
    #         #print(dist)
    #         #print(real_height, ' meter')
            
            
    #         #按Q就會拍照
    #         if cv.waitKey(1) == ord('q'):
    #             break
    #     color_save_img = Image.fromarray(np.uint8(color_img))
    #     color_save_img.save("tmp/color_tmp.jpg","JPEG")
    #     #print('height,width' , (height,width))
    #     real_height_map = np.zeros((height,width))
    #     for y in range(width):
    #             for x in range(height):
    #                 real_height_map[x][y] = original_height_map[x][y] - depth.get_distance(y, x)

        
    # # print("10101")
    # # 先做一個假的
    # height = 35
    # width = 25
    # real_height_map = np.zeros((height,width))
    # for y in range(width):
    #     for x in range(height):
    #         real_height_map[x][y] = 1

    
    # File name to read the data
    # file_name = 'interface/forUnet2.csv'
    file_name = 'forUnet.csv'

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

    # print("height: ", after_height)
    # print("width: ", atfer_width)
    # print("\n2D Double Array:")
    # for row in after_real_height_map:
    #     print(row)


    

    unet = Unet()

    
        
    #放進模型切割
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
    print("mask_width, mask_height",(mask_width, mask_height))
    
    
    #由灰度圖來辨別食物的位置
    total_height = np.zeros(classes_num, dtype=float)
    target_imgs = [np.zeros((after_height, after_width, 3), dtype=np.uint8) for _ in range(classes_num)]
    for y in range(mask_width):
                for x in range(mask_height):
                    pixel_value = mask.getpixel((y,x))
                    (target_imgs[pixel_value])[x][y] = (0, 0, 255)
                    #if (real_height_map[x][y] > critical_height_value):
                    total_height[pixel_value] += after_real_height_map[x][y]

        
        
    # print("32323")
                    
                    
    

    weight_a = -0.00005
    weight_b = 0.3504
    weight_c = 1.8748
    volume = []
    for i in range(1,classes_num):
        # volume = total_height[i] * total_height[i]*weight_a +total_height[i]*weight_b+weight_c
        volume.append(total_height[i] * total_height[i]*weight_a +total_height[i]*weight_b+weight_c)
        #volume = total_height[i]
        
        #volume = round(volume,4)
        # print("class_name:" + str(name_classes[i]) + " volume:" + str(volume) + " cm^3")
    
    # for i in range(1,classes_num):
    #     cv.imwrite(f"unet_web/result/target_img_{i}.png",target_imgs[i])
    # for i in range(1,classes_num):
    #     #volume = total_height[i]
        
    #     #volume = round(volume,4)
    #     print("class_name:" + str(name_classes[i]) + " volume:" + str(total_height[i]) + " cm^3")
    

    # pipeline.stop()




    # output_data = [3.123, 5.567, 4.789]
    # print(output_data)
        
    # print(volume)








# win = tk.Tk()

# def display_matrix(food_info):
#     for i in range(len(food_info)):
#         for j in range(len(food_info[i])  - 1 ):
#             if(str(food_info[i][1]) == '0.0'): 
#                 label = tk.Label(frame, text="")
#             else:
#                 label_text = str(food_info[i][j])
#                 label = tk.Label(frame, text=label_text, borderwidth=1, bg = "skyblue",fg = "black", relief="solid", width=10, height=2)
#                 label.config(font="微軟正黑體 10")
#                 label.grid(row=i, column=j)

# 省略部分代码...
class_name = ["wafer_pie", "oreo", "yuki" , "snow_craker", "rice_craker", "rye_biscuit"]

food_info =[
    ['食物種類',	'重量(g)',	'熱量(Cal)',	'蛋白質(g)',	'碳水化合物(g)', '脂防(g)','價格(元))'],
    ['新貴派',   10.138,  55.034,  1.11,    5.407,  3.234 , 4.655],
    ['oreo',        9.2,	  45,	   0.433,	6.567,	1.9, 3.296],
    ['yuki',        9.35,	  47.85,   0.6,	    6.05,	2.35, 3.563],
    ['雪餅', 7.917,	  39.375,  0.354,	5.75,	1.667, 2.958],
    ['旺旺仙貝', 3.387,	  16.145,  0.147,	2.529,	0.61, 1.048],
    ['黑麥口糧', 8.182,	  33.082,  0.6,	    6.055,	0.791, 1.091]
]



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


for i in range(6):
    for j in range(6):
        food_info[i+1][j+1] = round(float(volume[i])*float(food_info[i+1][j+1]), 2)

total_price = 0
total_weight = 0
total_cal = 0
for i in range(6):
    total_price += food_info[i+1][6] 
    total_weight += food_info[i+1][1]
    total_cal += food_info[i+1][2]
show_on_cashier = [total_price, total_weight, total_cal]
print(show_on_cashier)


show = [[0 for j in range(5)] for i in range(6)]
for j in range(6):
    for i in range(5):
        show[j][i] = food_info[j+1][i+1]
print(show)


# RGB_img = ImageTk.PhotoImage(Image.open("tmp/color_tmp.jpg").resize((320, 240)))
# seg_img = ImageTk.PhotoImage(Image.open("result/blend_img.png").resize((320, 240)))

# win.title("3D 智助餐")
# win.geometry("1000x620")
# win.config(bg = "#323232")
# win.iconbitmap("logo.ico")

# img_label = tk.Label(image= RGB_img)
# img_label.place(anchor=tk.CENTER,  x = 250, y = 150 )
# img_text = tk.Label(text= "RGB影像", bg = "#323232", fg = "skyblue" , font="微軟正黑體 20")
# img_text.place(anchor=tk.CENTER, x = 250, y = 300 )



# seg_label = tk.Label(image= seg_img)
# seg_label.place(anchor=tk.CENTER,  x = 250, y = 450)
# seg_text = tk.Label(text= "分割結果", bg = "#323232", fg = "skyblue" , font="微軟正黑體 20")

# seg_text.place(anchor=tk.CENTER, x = 250, y = 600 )


# weight_text = tk.Label(text = "重量 : "+ str(round(total_weight, 3)) + " g", bg = "#323232", fg = "white" , font="微軟正黑體 24")
# cal_text = tk.Label(text = "熱量 : "+ str(round(total_cal, 3)) +" Cal ", bg = "#323232", fg = "white", font="微軟正黑體 24")
# price_text = tk.Label(text = "價錢 : "+ str(int(round(total_price, 0))) +" 元", bg = "#323232", fg = "white", font="微軟正黑體 24")

# print("重量 : "+ str(round(total_weight, 3)) + " g")
# print("熱量 : "+ str(round(total_cal, 3)) +" Cal ")
# print("價錢 : "+ str(int(round(total_price, 0))) +" 元")
# right_block_x = 700

# weight_text.place(anchor=tk.CENTER, x = right_block_x, y = 80)

# cal_text.place(anchor=tk.CENTER, x = right_block_x, y = 140)

# price_text.place(anchor=tk.CENTER, x = right_block_x, y = 200)

# frame = tk.Frame(win)  # 创建一个Frame来容纳表格
# frame.place(anchor=tk.CENTER, x = right_block_x, y = 440)  # 使用pack布局将Frame放在窗口中央

# display_matrix(food_info)

# win.mainloop()


# 寫入資料庫
# cName = '林三和'
# cSex =  'M'
# cBirthday =  '1987-12-26'
# cEmail = 'bear@superstar.com'
# cPhone =  '0963245612'
# cAddr =  '台北市信義路18號'
# unit = food_info.objects.create(cName=cName, cSex=cSex, cBirthday=cBirthday, cEmail=cEmail,cPhone=cPhone, cAddr=cAddr) 
# unit.save()

