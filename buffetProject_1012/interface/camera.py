# https://github.com/sawardekar/Django_VideoStream
import cv2 as cv
import pyrealsense2 as rs
import numpy as np


class FoodVedioCamera(object):
    def __init__(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        #調整解析度
        self.config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        self.config.enable_device('f0233004')  
        # 啟動深度攝影機
        self.profile = self.pipeline.start(self.config) 
    
    def __del__(self):
        self.pipeline.stop()
    
    def get_frame(self):
        # 影像
        # 取得照片frame
        frame = self.pipeline.wait_for_frames()
        # 把兩種frames對齊
        color = frame.get_color_frame()
        # 轉換成圖片img
        color_img = np.asanyarray(color.get_data())

        # 左右翻轉
        frame_flip = cv.flip(color_img, 1)
        # 把矩陣轉為jpg檔案格式
        ret, jpeg = cv.imencode('.jpg', frame_flip)
        # 回傳字結數組(使用它才能用於網路傳輸 文件儲存等操作)
        return jpeg.tobytes()


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

