from machine import ADC, Pin, UART
import utime

# PINS to be initialized
PINS = [18, 19, 20, 21]

for i in PINS:
    Pin(i, Pin.OUT) # SETUP EACH PIN
    print("GPIO PIN", i, " SETUP")
    
# Init ADC PIN
Sig = ADC(28)

# Init UART
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
uart.init(baudrate=115200, bits=8, parity=None, stop=1)

# Init counter
count = 0

while True:
    
    # SET PINS BASED OFF COUNT
    Pin(PINS[0], value = (count & 0x01))
    Pin(PINS[1], value = (count & 0x02))
    Pin(PINS[2], value = (count & 0x04))
    Pin(PINS[3], value = (count & 0x08))
    
    # get the adc reading
    reading = Sig.read_u16()
    print("ADC ", count, " : ", reading)
    
    if reading < 48000: # if reading is lower than adc value
        uart.write(b'%d'%count) # send count data to PI
        print(count, "SENT!")
    
    utime.sleep(0.1) # sleep for a short time (0.1s)
    count = (count + 1) % 9 # LOOP PINS 0-9