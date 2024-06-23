"""

偵測按鈕是否被按下

"""



import serial
from django.http import JsonResponse


def changePage(request):
    if request.method == "GET":
        # 初始化串口通信
        serial_port = 'COM3'  # 修改为你的串行端口
        ser = serial.Serial(serial_port, 9600, timeout=1)

        try:
            while True:
                # 从串行端口读取一行数据
                line = ser.readline().decode('utf-8').strip()
                    
                if "red" in line:
                    ser.close()
                    print("red_btn is clicked")
                    return JsonResponse({'btn': 'red'})
                if "black" in line:
                    ser.close()
                    print("black_btn is clicked")
                    return JsonResponse({'btn': 'black'})
        except KeyboardInterrupt:
            print("Program terminated by user.")
        finally:
            ser.close()  # 关闭串行端口
        
        

