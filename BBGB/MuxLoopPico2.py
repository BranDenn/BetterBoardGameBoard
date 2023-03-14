from machine import ADC, Pin, UART, SPI, Timer
from ST7735 import TFT
from sysfont import sysfont
import time

# Player Stats
player1_wins = 0
player2_wins = 0

def update_player1(pin) -> void:
    global player1_wins
    player1_wins += 1
    update_display()
    vibration()
    
def update_player2(pin) -> void:
    global player2_wins
    player2_wins += 1
    update_display()
    vibration()

# MUX_PINS to be initialized
MUX_PINS = [18, 19, 20, 21]

for i in MUX_PINS:
    Pin(i, Pin.OUT) # SETUP EACH PIN
    print("GPIO PIN", i, " SETUP")
   
player1_pin = Pin(2, Pin.IN, Pin.PULL_DOWN) # set pin for player1 interrupt
player1_pin.irq(update_player1, Pin.IRQ_RISING) # call update_player1 function on interrupt
player2_pin = Pin(3, Pin.IN, Pin.PULL_DOWN) # set pin for player2 iterrupt
player2_pin.irq(update_player2, Pin.IRQ_RISING) # call update_player2 function on interrupt

# Init vibration
vibration_timer = Timer() # timer for vibration
vibrate = Pin(5, Pin.OUT)

def stop_vibration(time) -> None:
    print("stopping vibration")
    vibrate.value(0)

def vibration() -> None:
    time = 2500
    print("starting vibration for ", time, "ms")
    vibrate.value(1)
    vibration_timer.init(mode = Timer.ONE_SHOT, period = time, callback = stop_vibration) 
    
# Init ADC PIN
Sig = ADC(28)

# Init UART
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
uart.init(baudrate=115200, bits=8, parity=None, stop=1)

# Sensor Positions
#HFX_POSITIONS = [50, 51, 52, 57, 58, 59, 60, 61, 62, 63]
HFX_POSITIONS = [0, 1, 2, 3, 4, 5, 6]
#HFX_POSITIONS = [0, 1, 9, 10, 11, 12, 13]

# Init LCD
spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi, 14, 15, 16)
tft.initr()
tft.rgb(True)

def update_display() -> None:
    tft.text((5, 15), "Blue Points: %d" %player1_wins, TFT.WHITE, sysfont, 1)
    tft.text((5, 30), "Red Points: %d" %player2_wins, TFT.WHITE, sysfont, 1)

tft.fill(TFT.BLACK)
update_display()

while True:   
    for count in range(len(HFX_POSITIONS)):
         # SET MUX_PINS BASED OFF COUNT
        Pin(MUX_PINS[0]).value(count & 0x01)
        Pin(MUX_PINS[1]).value(count & 0x02)
        Pin(MUX_PINS[2]).value(count & 0x04)
        Pin(MUX_PINS[3]).value(count & 0x08)
        reading = Sig.read_u16()

            # get the adc reading
        print("MUX 0 ADC ", count, " : ", reading)
            
        if reading < 45000: # if reading is lower than adc value
            if(HFX_POSITIONS[count] > 9):
                uart.write('t') # send count data to PI

            uart.write(b'%d'%HFX_POSITIONS[count]) # send count data to PI           uart.write('hello')
            print("SENT DATA FOR HFX PIN: ", HFX_POSITIONS[count])

        time.sleep(0.1) # sleep for a short time (0.1s)
