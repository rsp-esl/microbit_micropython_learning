from microbit import *

addr = 0x45  # set 7-bit address of SHT3x-DIS

# see: https://github.com/ralf1070/Adafruit_Python_SHT31/
################################################################

def crc8(buf):
    """ Polynomial 0x31 (x8 + x5 +x4 +1) """
    polynom = 0x31;
    crc = 0xff;
    for i in range(0, len(buf)):
        crc ^= buf[i]
        for j in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ polynom
            else:
                crc = (crc << 1)
    return (crc & 0xff)

################################################################

print( '\nSHT3x-DIS temperature & relative humidty sensor reading...' )
print( 'Press the button A to start!\n' )
display.show( Image.ARROW_W )

while True:
    if button_a.was_pressed():
        display.show('.')
        break

# send a soft-reset command
i2c.write( addr, bytearray([0x30,0xa2]) )

cnt = 0
while True:
    retries = 0
    raw = None
    running = True
    display.show( 'M' )
    sleep(1000)
    while running:
        try:
            # send command: measurement, high repeatability, with clock stretching 
            i2c.write( addr, bytearray([0x2c,0x06]) )
            sleep(150)
            # read 6 bytes: 
            #   Temperature: MSB, LSB, CRC8
            #   Humidity: MSB, LSB, CRC8
            raw = i2c.read(addr, 6)
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
            cnt   = cnt + 1 
            if crc8(raw[0:2]) != raw[2]: # CRC8 mismatch
                display.show( 'E' )
                temp_str = 'Temp.: --.-- deg.C'
            else:
                temp = -45 + (175 * ((raw[0] << 8) + raw[1]) / 65535.0)
                temp_str = 'Temp.: {0:0.2f} deg.C'.format( temp ) 
                
                
            if crc8(raw[3:5]) != raw[5]: # CRC8 mismatch
                display.show( 'E' )
                humid_str = 'Rel.Humid.: --.-- %RH'
            else:
                humid = 100 * ((raw[3] << 8) + raw[4]) / 65535.0
                humid_str = 'Rel.Humid.: {0:0.2f} %RH'.format( humid )
                
            print( '{0:4}) {1}, {2}'.format(cnt,temp_str,humid_str) )

    sleep(1000)

#############################################################
