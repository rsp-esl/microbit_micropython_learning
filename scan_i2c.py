from microbit import *

def scan_i2c():
    while True:
        print("Scanning I2C bus...")
        for i in range(0x01, 0x7f):
            try:
                i2c.read(i, 1)
            except OSError:
                pass
            else:
                print("Found a device at address: 0x{0:02x}".format(i) )
        print("Scanning complete")
    sleep(10)

scan_i2c()
sleep(3000)

