from django.shortcuts import render
from django.http.response import StreamingHttpResponse

import cv2 as cv
import pyrealsense2 as rs
import numpy as np
import keyboard
import csv
import os

# Create your views here.

class FoodVedioCameraCalib(object):
    def __init__(self):
        # self.flag = True
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

        # file_name = './static/file/original_height_map.csv'
        # self.original_height_map = []
        # with open(file_name, mode='r') as file:
        #     reader = csv.reader(file)
        #     for row in reader:
        #         self.original_height_map.append(row)

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
        if keyboard.is_pressed('c'):
            cv.imwrite(f"./static/image/screenShot.jpg" ,color_img)
            cv.imwrite(f"./unet_web/tmp/screenShot.jpg" ,color_img)
            self.plant_depth()
            # if self.flag == True:
            #     self.plant_depth()
            #     self.flag = False
            # else:
            #     self.food_depth()
            #     self.flag = True
        
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
    
    # def food_depth(self):
    #     self.real_height_map = np.zeros((self.height,self.width))
    #     for y in range(self.width):
    #         for x in range(self.height):
    #             self.real_height_map[x][y] = self.original_height_map[x][y] - self.depth.get_distance(y, x)

        # # Data to be written to the CSV file
        # dataForUnet = [
        #     ['height', self.height],
        #     ['width', self.width],
        #     [],  # Empty row for separation
        #     ['real_height_map'],  # Label for the 2D array
        # ]
        # dataForUnet.extend(self.real_height_map)  # Adding the 2D double array to the data list
        # with open("./static/file/forUnet.csv", mode="w", newline='') as file:
        #     # file.truncate(0)
        #     writer = csv.writer(file)
        #     writer.writerows(dataForUnet)

        # 如果 merge_data.txt 存在，就刪掉它
        file_path = './static/file/original_height_map.csv'
        if os.path.exists(file_path):
            os.remove(file_path)
        
        with open("./static/file/original_height_map.csv", mode="w", newline='') as file:
            file.truncate(0)
            writer = csv.writer(file)
            writer.writerows(self.original_height_map)
        np.savetxt("./static/file/original_height_map.csv", self.original_height_map, delimiter=",")


# 設置 camera (要把模型放進去應該去camera.py寫)
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# 連接攝影機(特定語法，應該，我是複製貼上)，gen(camera.py中的class)
def FoodVedioFeedCalib(request):
    return StreamingHttpResponse(gen(FoodVedioCameraCalib()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

# 校正空盤的頁面
def calib(request):
    return render(request, 'calibration\\calib.html')