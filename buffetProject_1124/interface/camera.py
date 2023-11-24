# https://github.com/sawardekar/Django_VideoStream
# 底下4個import都需要用pip下載外包套件
import cv2 as cv
import pyrealsense2 as rs
import numpy as np
import keyboard

import csv


class FoodVedioCamera(object):
    def __init__(self):
        self.flag = True
        # self.count = 1
        # self.key = cv.waitKey(1) 
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        #調整解析度
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.config.enable_device('f0233004')
        
        #對齊像素
        align_to = rs.stream.color
        self.align = rs.align(align_to)

        # 啟動深度攝影機
        self.profile = self.pipeline.start(self.config)
    
        # 取得深度攝影機的sensor物件
        self.depth_sensor = self.profile.get_device().first_depth_sensor()
        self.depth_sensor.set_option(rs.option.visual_preset,5)

        # 設定最大和最小深度值
        self.colorizer = rs.colorizer()
        self.colorizer.set_option(rs.option.visual_preset, 1) # 0=Dynamic, 1=Fixed, 2=Near, 3=Far
        self.colorizer.set_option(rs.option.min_distance, 0.3)
        self.colorizer.set_option(rs.option.max_distance, 2.7)
        self.colorizer.set_option(rs.option.histogram_equalization_enabled, True)

    def __del__(self):
        self.pipeline.stop()
    
    def get_frame(self):
        # 影像
        # 取得照片frame
        frame = self.pipeline.wait_for_frames()
        # 把兩種frames對齊
        aligned_frames = self.align.process(frame)
        self.depth = aligned_frames.get_depth_frame()
        color = aligned_frames.get_color_frame()
        # 轉換成圖片img
        self.depth_img = np.asanyarray(self.depth.get_data())
        color_img = np.asanyarray(color.get_data())

        

        self.depth_colormap = np.asanyarray(self.colorizer.colorize(self.depth).get_data())
        #取得寬高
        self.width = self.depth.get_width()
        self.height = self.depth.get_height() 
        
        #按s就會拍照
        if keyboard.is_pressed('s'):
            cv.imwrite(f"./static/image/screenShot.jpg" ,color_img)
            cv.imwrite(f"./unet_web/tmp/screenShot.jpg" ,color_img)
            # if self.count == 1:
            if self.flag == True:
                self.plant_depth()
                # self.count += 1
                self.flag = False
            else:
                self.food_depth()
                # self.count += 1
                self.flag = True
        
        # 左右翻轉
        # frame_flip = cv.flip(color_img, 1)
        # 把矩陣轉為jpg檔案格式
        ret, jpeg = cv.imencode('.jpg', color_img)
        
        # 回傳字結數組(使用它才能用於網路傳輸 文件儲存等操作)
        return jpeg.tobytes()
    
    def plant_depth(self):
        self.original_height_map = np.zeros((self.height,self.width))
        for y in range(self.width):
            for x in range(self.height):
                self.original_height_map[x][y] = self.depth.get_distance(y, x)
        self.get_frame()
    
    def food_depth(self):
        self.real_height_map = np.zeros((self.height,self.width))
        for y in range(self.width):
            for x in range(self.height):
                self.real_height_map[x][y] = self.original_height_map[x][y] - self.depth.get_distance(y, x)

        # Data to be written to the CSV file
        dataForUnet = [
            ['height', self.height],
            ['width', self.width],
            [],  # Empty row for separation
            ['real_height_map'],  # Label for the 2D array
        ]
        dataForUnet.extend(self.real_height_map)  # Adding the 2D double array to the data list
        with open("forUnet.csv", mode="w", newline='') as file:
            file.truncate(0)
            writer = csv.writer(file)
            writer.writerows(dataForUnet)

# 廚餘區，因為沒用到，忽略
class WasteVedioCamera(object):
    def __init__(self):
        self.video = cv.VideoCapture(1)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        frame_flip = cv.flip(image, 1)
        ret, jpeg = cv.imencode('.jpg', frame_flip)
        return jpeg.tobytes()

