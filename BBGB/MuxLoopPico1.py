from machine import ADC, Pin, UART
import time

# PINS to be initialized
MUX_PINS = [10, 11, 12, 13, 18, 19, 20, 21]

for i in MUX_PINS:
    Pin(i, Pin.OUT) # SETUP EACH PIN
    print("GPIO PIN", i, " SETUP")
    
# Init ADC PIN
Sig = ADC(28)

# Init UART
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
uart.init(baudrate=115200, bits=8, parity=None, stop=1)

# Sensor Positions
HFX_POSITIONS = [7, 8, 9, 10, 11, 12, 13]

while True:
    for count in range(len(HFX_POSITIONS)):
         # SET MUX_PINS BASED OFF COUNT
        Pin(MUX_PINS[0]).value(count & 0x01)
        Pin(MUX_PINS[1]).value(count & 0x02)
        Pin(MUX_PINS[2]).value(count & 0x04)
        Pin(MUX_PINS[3]).value(count & 0x08)
        reading = Sig.read_u16()

            # get the adc reading
        print("MUX 1 ADC ", count, " : ", reading)
            
        if reading < 45000: # if reading is lower than adc value
            uart.write(b'%d'%HFX_POSITIONS[count]) # send count data to PI
            print("SENT DATA FOR HFX PIN: ", HFX_POSITIONS[count])

        time.sleep(0.1) # sleep for a short time (0.1s)
            

