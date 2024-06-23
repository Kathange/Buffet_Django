"""

此為拍攝照片的處理，需按下兩次 "s" 鍵，進行拍攝

"""


# https://github.com/sawardekar/Django_VideoStream
import cv2 as cv
import pyrealsense2 as rs
import numpy as np
import csv
import serial
from django.http import JsonResponse



time = 25
count2 = 0
distance = 100
dis = 12

# 空盤已記錄，使用超音波偵測 擷取並分析
class FoodVedioCamera(object):
    def __init__(self):
        self.flag = True
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

        # 初始化串口通信
        serial_port = 'COM3'  # 修改为你的串行端口
        self.ser = serial.Serial(serial_port, 9600, timeout=1)
        # self.time = 10 # 一次0.5sec 用來控制時間
        # self.dis = 10 # 用來控制偵測距離 (cm)
        # self.count = 0  # 用于计数连续小于100cm的次数

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
        
        # #按s就會拍照
        # if keyboard.is_pressed('s'):
        #     cv.imwrite(f"./static/image/screenShot.jpg" ,color_img)
        #     cv.imwrite(f"./unet_web/tmp/screenShot.jpg" ,color_img)
        #     self.food_depth()
        
        # 如果偵測超過5秒，即可開始截取並偵測
        # ultra = self.ultrasound()
        # ultraLoad = json.loads(ultra)
        # capture = json.dumps(ultraLoad)
        # if capture["capture"] == "yes":
        # print("ultra check")
        if self.ultrasound() == True:
            self.ser.close()
            cv.imwrite(f"./static/image/screenShot.jpg" ,color_img)
            cv.imwrite(f"./unet_web/tmp/screenShot.jpg" ,color_img)
            self.food_depth()
        
        # 左右翻轉
        # frame_flip = cv.flip(color_img, 1)
        # 把矩陣轉為jpg檔案格式
        ret, jpeg = cv.imencode('.jpg', color_img)
        
        # 回傳字結數組(使用它才能用於網路傳輸 文件儲存等操作)
        return jpeg.tobytes()
    
    def food_depth(self):
        # 讀取空盤深度資訊
        original_height_map = np.zeros((640,480))
        file_name = './static/file/original_height_map.csv'
        original_height_map = np.loadtxt(file_name, delimiter=',')

        self.real_height_map = np.zeros((self.height,self.width))
        for y in range(self.width):
            for x in range(self.height):
                self.real_height_map[x][y] = original_height_map[x][y] - self.depth.get_distance(y, x)

        # Data to be written to the CSV file
        dataForUnet = [
            ['height', self.height],
            ['width', self.width],
            [],  # Empty row for separation
            ['real_height_map'],  # Label for the 2D array
        ]
        dataForUnet.extend(self.real_height_map)  # Adding the 2D double array to the data list
        with open("./static/file/forUnet.csv", mode="w", newline='') as file:
            file.truncate(0)
            writer = csv.writer(file)
            writer.writerows(dataForUnet)

    def ultrasound(self):
        global count2
        global distance
        global dis
        try:
            # while True:
                # 从串行端口读取一行数据
                line = self.ser.readline().decode('utf-8').strip()
                if line.startswith("Distance in CM:"):
                    # 提取距离值
                    distance = int(line.split(":")[1].strip())
                    print(f"Detected distance: {distance} cm")  # 打印距离

                    # 检查距离是否小于100cm
                    if distance < dis:
                        # print("count2 + 1")
                        count2 += 1
                    else:
                        count2 = 0  # 如果距离不小于100cm，重置计数

                    # 如果连续超过20次小于100cm，则发送警告
                    if count2 > time:
                        print("餐盤在這裡待了5秒")
                        # 在这里执行发送信号的代码
                        # self.count = 0  # 可选：发送警告后重置计数，避免连续发送警告
                        return True
                return False

        except KeyboardInterrupt:
            print("Program terminated by user.")
        
        return False



def capture(request):
    global count2
    global distance
    global dis
    if request.method == 'GET':
        # print("work")
        if count2 > time:
            print("capture in~~")
            count2 = 0
            distance = 100
            return JsonResponse({'capture': "yes", 'distance': "notmind"})
        # print("not yet")
        if distance < dis:
            return JsonResponse({'capture': "no", 'distance': "small"})
        else:
            return JsonResponse({'capture': "no", 'distance': "big"})
    



