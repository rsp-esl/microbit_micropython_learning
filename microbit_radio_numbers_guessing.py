# Author: Rawat S. (https://github.com/rsp-esl/)
# Date: 2018-09-25

from microbit import *
import random
import radio

radio.on()
radio.config(channel=19)
radio.config(power=7)

sleep(500)
if button_b.is_pressed():
    sender = True
    display.scroll( 'Sender')
else:
    sender = False
    display.scroll( 'Receiver' )

n = 10
random.seed( pin0.read_analog() )
selected = set() # used to keep a list of selected numbers
msg = '  '
while True:
    if button_a.was_pressed():
        display.clear()
        while True:
            x = random.randint(1,n) # 1..10
            if x not in selected:
                selected.add( x )
                break
        msg = "%02d" % x
        display.scroll(msg, 200)
        print (msg)
        if sender:
            radio.send( msg )
        if len(selected) == n:
            selected = set()
            msg = '  '
    else:
        recv_msg = radio.receive()
        if recv_msg == msg:
             display.show(Image.HAPPY)
        elif button_b.was_pressed():
             if sender:
                radio.send( msg )
             display.scroll(msg)
