import serial
import time
uart = serial.Serial("/dev/ttyS0", baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout = 1)

uart.flush()
while True:
    try:
        print("waiting for uart...")
        #uart.flush()
        data = uart.readline()
        print(data)
        #time.sleep(0.5)
        if data:
            print(int(data))
        else:
            print('timeout')
    except Exception as e:
        print("EXCEPTION HIT:", e)
        break
