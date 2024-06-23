import serial

# 初始化串口通信
serial_port = 'COM5'  # 修改为你的串行端口
ser = serial.Serial(serial_port, 9600, timeout=1)

def main():
    time = 10 # 一次0.5sec 用來控制時間
    dis = 100 # 用來控制偵測距離 (cm)
    count = 0  # 用于计数连续小于100cm的次数
    try:
        while True:
            # 从串行端口读取一行数据
            line = ser.readline().decode('utf-8').strip()
            if line.startswith("Distance in CM:"):
                # 提取距离值
                distance = int(line.split(":")[1].strip())
                print(f"Detected distance: {distance} cm")  # 打印距离

                # 检查距离是否小于100cm
                if distance < dis:
                    count += 1
                else:
                    count = 0  # 如果距离不小于100cm，重置计数

                # 如果连续超过20次小于100cm，则发送警告
                if count > time:
                    print("餐盤在這裡待了5秒")
                    # 在这里执行发送信号的代码
                    count = 0  # 可选：发送警告后重置计数，避免连续发送警告
            if "Card UID:" in line:
            # 提取 UID 部分
                uid_value = line.split(":")[1].strip()
                print(f"Read UID: {uid_value}")
                
            if "red" in line:
                print("red_btn is clicked")
            if "black" in line:
                print("black_btn is clicked")
    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        ser.close()  # 关闭串行端口

if __name__ == "__main__":
    main()
