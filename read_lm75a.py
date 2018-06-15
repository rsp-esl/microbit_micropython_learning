from microbit import *

addr = 0x48   # set 7-bit address of LM75A 

print( '\nLM75A temperature sensor reading...' )
print( 'Press the button A to start!\n' )
display.show( Image.ARROW_W )

while True:
    if button_a.was_pressed():
        display.show( ' ' )
        break

cnt = 0
while True:
    retries = 0
    raw = None
    running = True
    display.show( 'M' )
    sleep(1000)
    while running:
        try:
            raw = i2c.read(addr, 2) # read two bytes (MSB followed by LSB)
        except Exception:
            retries = retries + 1
            if retries > 5:
                display.show( 'E' )
                print( 'I2C reading error...' )
                running = False
            else:
                sleep(500)
        else:
            display.show( ' ' )
            running = False

        if raw is not None:
            cnt = cnt + 1
            value = (((raw[0] << 8) + raw[1]) >> 7) 
            temp  = int(value) * 0.5
            print( '{0:4}) Temperature: {1:0.1f} deg.C'.format(cnt,temp) )

    sleep(1000)

#############################################################
