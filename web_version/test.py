import serial  # 引用pySerial模組
import time

##COM_PORT = 'COM47'    # 指定通訊埠名稱
#BAUD_RATES = 9600    # 設定傳輸速率
#ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠
#ser.write((bytes("1",encoding='utf-8')))
#time.sleep(10) 
#while True:
  #ser.write((bytes("3",encoding='utf-8')))
  #time.sleep(5)

import serial
import time

SerialObj = serial.Serial('COM5') # COMxx   format on Windows
                                  # ttyUSBx format on Linux

SerialObj.baudrate = 9600  # set Baud rate to 9600
SerialObj.bytesize = 8     # Number of data bits = 8
SerialObj.parity   ='N'    # No parity
SerialObj.stopbits = 1     # Number of Stop bits = 1
time.sleep(3)

SerialObj.write(b'3')      #transmit 'A' (8bit) to micro/Arduino
SerialObj.close()          # Close the port