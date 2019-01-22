# Author: Rawat S. (https://github.com/rsp-esl/)

from microbit import  *

def bin_str(n):
  fp = "{0:0" + str(n) + "b}"
  return [fp.format(i) for i in range(2**n) ]

state = 0
index = 0
nlist = [2,3,4]  # a list of selectable values of n
i = 0
n = nlist[i]

while True:
  display.show( str(n) )
  if state == 0: # idle/input state
    if button_a.was_pressed(): # press the button 'A' to change n
      i = (i+1) % len(nlist)
      n = nlist[i]
      display.show( str(n) )         # show the current value of n
    if button_b.was_pressed(): # press the button 'B' to start display 
      bits = bin_str(n)              # generate a list bit strings
      state = 1                      # goto state 1
      index = 0                      # reset the value of index 
  elif state == 1: # display state
    msg = bits[index]                # convert list to string
    print( msg )                     # print the bit string
    display.scroll( msg, delay=150 ) # display the bit string
    index += 1                       # increment the index variable
    if index == len(bits):           # the bit string is reached
      state = 2                      # goto state 2
  elif state == 2: # done state
    display.show( Image.HAPPY )      # show the happy face
    sleep( 1000 )                    # wait for 1 second 
    state = 0                        # goto state 0
  sleep(100)
