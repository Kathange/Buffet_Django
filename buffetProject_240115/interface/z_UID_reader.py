import serial
import time
# from gpiozero import Buzzer

# 调整串口设备的名称，具体名称可在设备管理器中查看
serial_port = 'COM7'  # 将 x 替换为你的 Arduino 分配的串口号
# On Windows:
# Press Win + X and select "Device Manager."
# Look for "Ports (COM & LPT)" to see a list of available COM ports.
# check "USB serial ports" is COM?
# 左右的USB接口都可以用

# 初始化串口通信
ser = serial.Serial(serial_port, 9600, timeout=1)


try:
    print("please put card")
    while True:
        # 读取串口数据
        line = ser.readline().decode('utf-8').strip()

        # 如果数据包含 "UID Value:"，表示读取到 UID
        if "UID Value:" in line:
            # 提取 UID 部分
            uid_value = line.split(":")[1].strip()
            print(f"Read UID: {uid_value}")
            break

        # 可以加入其他处理逻辑，视你的需求而定

except KeyboardInterrupt:
    # 用户按下 Ctrl+C 时，中断循环
    print("Program terminated by user.")

finally:
    # 关闭串口
    ser.close()
    