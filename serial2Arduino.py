import serial
import time

# 創建串口對象，並設定波特率為 9600
# 你需要根據你的系統和 Arduino 的連接端口來修改 'COM3'。例如，在 Linux 上，它可能是 '/dev/ttyUSB0'
arduino = serial.Serial('COM47', 9600)

time.sleep(2)  # 等待串口連接

while True:
  num=input("請輸入 1 or 2:")
  if(num=="1"):
    arduino.write(b'1')  # 發送 '1' 來打開 LED
  elif(num=="2"):    
    arduino.write(b'2')  # 發送 '0' 來關閉 LED

# 測試


arduino.close()  # 關閉串口連接