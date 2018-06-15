from microbit import *

addr = 0x52  # 7-bit address of the Wii Nunchuck 

sleep(1000)
print( 'Micro:Bit Wii Nunchuck Interfacing (I2C)' )
print( 'Press the button A to start!' )
display.show( Image.ARROW_W )

while True:
    if button_a.was_pressed():
        display.show( ' ' )
        break

i2c.write( addr, bytearray( [0x40,0x00] ) )
sleep(100)

DELTA_MIN = 5

cnt = 0
xc, yc = None, None
while True:
    retries = 0
    raw = None
    running = True
    sleep(200)
    while running:
        try:
            i2c.write( addr, bytearray([0x00]) )
            sleep(50)
            raw = i2c.read( addr, 6 )
        except Exception:
            retries = retries + 1
            if retries > 5:
                display.show( 'E' )
                print( 'I2C reading error...' )
                running = False
            else:
                sleep(500)
        else:
            running = False

        if raw is not None:
            cnt = cnt + 1
            data = [(0x17 + (0x17 ^ raw[i])) for i in range(6)]
            x,y = data[0],data[1]
            ax,ay,az = data[2],data[3],data[4]
            if xc == None:
                xc = x
            if yc == None:
                yc = y
            dx, dy = (x-xc),(y-yc)
            if (dx < -DELTA_MIN):
                print('West: %d' % abs(dx) )
            elif (dx > DELTA_MIN):
                print('East: %d' % abs(dx) )
                
            if (dy < -DELTA_MIN):
                print('South: %d' % abs(dy) )
            elif (dy > DELTA_MIN):
                print('North: %d' % abs(dy) )

            print('Joystick XY : %d %d' % (x,y) )
            print('Accel. XYZ  : %d %d %d' % (ax,ay,az) )
            if (data[5] & 0x02) == 0:
                print('Button C    : pressed' )
            if (data[5] & 0x01) == 0:
                print('Button Z    : pressed' )

    sleep(100)

#############################################################
