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

if __name__ == "__main__":
    #predict setting
    count           = True
    name_classes    = ['_background_','wafer_pie', 'oreo', 'yuki', 'snow_cracker', 'rice_cracker', 'rye_biscuit']
    classes_num     = 7
    
    critical_height_value = 0.003 #過濾空白處的值
    # setting
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
    config.enable_device('f0233004')

    #對齊像素
    align_to = rs.stream.color
    align = rs.align(align_to)

    # 啟動深度攝影機
    profile = pipeline.start(config)

    # 取得深度攝影機的sensor物件
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_sensor.set_option(rs.option.visual_preset,5)


    # 設定最大和最小深度值
    colorizer = rs.colorizer()
    colorizer.set_option(rs.option.visual_preset, 1) # 0=Dynamic, 1=Fixed, 2=Near, 3=Far
    colorizer.set_option(rs.option.min_distance, 0.3)
    colorizer.set_option(rs.option.max_distance, 2.7)
    colorizer.set_option(rs.option.histogram_equalization_enabled, True)
    #depth_sensor.set_option(rs.option.max_distance, max_distance)

    #pipeline.start(config)
    #影像
    while True:
        #取得照片frame
        frame = pipeline.wait_for_frames()
        #把兩種frames對齊
        aligned_frames = align.process(frame)
        depth = aligned_frames.get_depth_frame()
        color = aligned_frames.get_color_frame()

        #轉換成圖片img
        depth_img = np.asanyarray(depth.get_data())
        color_img = np.asanyarray(color.get_data())
    
        # depth_cmap = cv.applyColorMap(cv.convertScaleAbs(depth_img, alpha = 0.25),cv.COLORMAP_JET)
    
        depth_colormap = np.asanyarray(colorizer.colorize(depth).get_data())
        #取得寬高
        width = depth.get_width()
        height = depth.get_height()


        #取得中心點
        # center = (int(width/2),int(height/2))
        #cv.circle(color_img, (center[0],center[1]), 4,(0,0,255),5)
        #cv.circle(depth_colormap, (center[0],center[1]), 4,(0,0,255),5)
        #距離
        # dist = depth.get_distance(center[0], center[1])
        #實際物品高度
        # real_height = camera_height - dist

        
        
        
        
        #顯示圖片
        cv.imshow('depth_colormap', depth_colormap)
        cv.imshow('rgb',color_img)
        
        #cv.imshow('depth',depth_cmap)
        #print(dist)
        #print(real_height, ' meter')
        
        
        #按Q就會拍照
        if cv.waitKey(1) == ord('q'):
            break

    original_height_map = np.zeros((height,width))
    for y in range(width):
            for x in range(height):
                #original_height_map[x][y] = 0.5
                original_height_map[x][y] = depth.get_distance(y, x)
                 




    #攝影機高度
    
    #影像
    for times in range(10) :
        while True:
            #取得照片frame
            frame = pipeline.wait_for_frames()
            #把兩種frames對齊
            aligned_frames = align.process(frame)
            depth = aligned_frames.get_depth_frame()
            color = aligned_frames.get_color_frame()

            #轉換成圖片img
            depth_img = np.asanyarray(depth.get_data())
            color_img = np.asanyarray(color.get_data())
        
            # depth_cmap = cv.applyColorMap(cv.convertScaleAbs(depth_img, alpha = 0.25),cv.COLORMAP_JET)
        
            depth_colormap = np.asanyarray(colorizer.colorize(depth).get_data())
            #取得寬高
            width = depth.get_width()
            height = depth.get_height()


            #取得中心點
            # center = (int(width/2),int(height/2))
            #cv.circle(color_img, (center[0],center[1]), 4,(0,0,255),5)
            #cv.circle(depth_colormap, (center[0],center[1]), 4,(0,0,255),5)
            #距離
            # dist = depth.get_distance(center[0], center[1])
            #實際物品高度
            # real_height = camera_height - dist

            
            
            
            
            #顯示圖片
            cv.imshow('depth_colormap', depth_colormap)
            cv.imshow('rgb',color_img)
            
            #cv.imshow('depth',depth_cmap)
            #print(dist)
            #print(real_height, ' meter')
            
            
            #按Q就會拍照
            if cv.waitKey(1) == ord('q'):
                break
        color_save_img = Image.fromarray(np.uint8(color_img))
        color_save_img.save("tmp/color_tmp.jpg","JPEG")
        #print('height,width' , (height,width))
        real_height_map = np.zeros((height,width))
        for y in range(width):
                for x in range(height):
                    real_height_map[x][y] = original_height_map[x][y] - depth.get_distance(y, x)

        
            
        

        unet = Unet()

        
            
        #放進模型切割
        img = "tmp/color_tmp.jpg"
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')

        else:
            r_image = unet.detect_image(image, count=count, name_classes=name_classes)
            r_image.show()
            r_image.save("result/blend_img.png", format="PNG")

        #mask灰度圖
        mask = Image.open("tmp/total_mask.png").convert('L')
        mask_width, mask_height = mask.size
        print("mask_width, mask_height",(mask_width, mask_height))
        
        #由灰度圖來辨別食物的位置
        total_height = np.zeros(classes_num, dtype=float)
        target_imgs = [np.zeros((height, width, 3), dtype=np.uint8) for _ in range(classes_num)]
        for y in range(mask_width):
                    for x in range(mask_height):
                        pixel_value = mask.getpixel((y,x))
                        (target_imgs[pixel_value])[x][y] = (0, 0, 255)
                        #if (real_height_map[x][y] > critical_height_value):
                        total_height[pixel_value] += real_height_map[x][y]

            
            
            
                        
                        
        

        weight_a = -0.00005
        weight_b = 0.3504
        weight_c = 1.8748
        for i in range(1,classes_num):
            volume = total_height[i] * total_height[i]*weight_a +total_height[i]*weight_b+weight_c
            #volume = total_height[i]
            
            #volume = round(volume,4)
            print("class_name:" + str(name_classes[i]) + " volume:" + str(volume) + " cm^3")
        
        for i in range(1,classes_num):
            cv.imwrite(f"result/target_img_{i}.png",target_imgs[i])
        for i in range(1,classes_num):
            #volume = total_height[i]
            
            #volume = round(volume,4)
            print("class_name:" + str(name_classes[i]) + " volume:" + str(total_height[i]) + " cm^3")
        

    pipeline.stop()


