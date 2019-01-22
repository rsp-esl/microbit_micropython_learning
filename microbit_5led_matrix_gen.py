# Author: Rawat S. (https://github.com/rsp-esl/)

from microbit import *
import random

# create an n x n matrix with random elements from {0,1}
def create_matrix( n ):
    m = [n*[0] for i in range(n)] # create a matrix filled with zeros
    selected = set()     # used to keep the row numbers already selected
    for col in range(n): # for each column of the matrix
        while True:
            row = random.randint(0,n-1)  # randomize a new row number
            if row not in selected: # The row number is not in the set.
               selected.add( row )  # add the row number to the set
               m[row][col] = 1      # set the element at (row,col) to 1
               break
    return m

x = pin0.read_analog()
random.seed( x ) # set the random seed using P0 analog input value
N = 5
autorunning = False

while True:
    if button_b.was_pressed():
        autorunning = not autorunning

    if button_a.is_pressed() or autorunning:
        display.clear()
        pixels = create_matrix(N)
        for r in range(N): # for each row
          for c in range(N): # for each column
            display.set_pixel(c, r, 9*(pixels[r][c]) )
        sleep( 500 )
    else:
        sleep(100)