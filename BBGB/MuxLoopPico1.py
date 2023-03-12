from machine import ADC, Pin, UART
import time

# PINS to be initialized
MUX_PINS = [10, 11, 12, 13, 18, 19, 20, 21]

for i in MUX_PINS:
    Pin(i, Pin.OUT) # SETUP EACH PIN
    print("GPIO PIN", i, " SETUP")
    
# Init ADC PIN
Sig0 = ADC(27)
Sig1 = ADC(28)

# Init UART
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
uart.init(baudrate=115200, bits=8, parity=None, stop=1)

# Sensor Positions
HFX_POSITIONS= [[2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16, 17, 18, 19, 24, 25],[26, 27, 28, 29, 30, 35, 36, 37, 38, 39, 40, 41, 46, 47, 48, 49]]

while True:
    for mux in range(2):
        #for i in PINS:
        #    Pin(i, value = 0) # SETUP EACH PIN
            
        for count in range(16):
            # SET PINS BASED OFF COUNT
            if mux == 0:
                continue
                Pin(MUX_PINS[0]).value(count & 0x01)
                Pin(MUX_PINS[1]).value(count & 0x02)
                Pin(MUX_PINS[2]).value(count & 0x04)
                Pin(MUX_PINS[3]).value(count & 0x08)
                reading = Sig0.read_u16()
    
            else:
                Pin(MUX_PINS[4]).value(count & 0x01)
                Pin(MUX_PINS[5]).value(count & 0x02)
                Pin(MUX_PINS[6]).value(count & 0x04)
                Pin(MUX_PINS[7]).value(count & 0x08)
                reading = Sig1.read_u16()

            # get the adc reading
            print("MUX ", mux, " ADC ", count, " : ", reading)
            
            if reading < 50000: # if reading is lower than adc value
                uart.write(b'%d'%HFX_POSITIONS[mux][count]) # send count data to PI
                print("SENT DATA FOR HFX PIN: ", HFX_POSITIONS[mux][count])

            time.sleep(0.5) # sleep for a short time (0.1s)
