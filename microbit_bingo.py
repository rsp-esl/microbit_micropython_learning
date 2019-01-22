# Author: Rawat S. (https://github.com/rsp-esl/)

from microbit import *
import random

BLINK_COUNT=10
N = 5

#####################################################################
# m = a nxn matrix with elements from {0,1}
#####################################################################

def blink_diag_major(n, dly=100):
    pause(1000)
    for j in range(BLINK_COUNT):
        for i in range(n):
            display.set_pixel( i, i, (j%2)*9 )
        sleep(dly) 

def blink_diag_minor(n, dly=100):
    sleep(10*dly)
    for j in range(BLINK_COUNT):
        for i in range(n):
            display.set_pixel( n-1-i, i, (j%2)*9 )
        sleep(dly) 

def blink_vertical(n, c, dly=100):
    sleep(10*dly)
    for j in range(BLINK_COUNT):
        for i in range(n):
            display.set_pixel( c, i, (j%2)*9 )
        sleep(dly) 

def blink_horizontal(n, r, dly=100):
    sleep(10*dly)
    for j in range(BLINK_COUNT):
        for i in range(n):
            display.set_pixel( i, r, (j%2)*9 )
        sleep(dly) 

#####################################################################
    
def check_diag_major(m,n):
    if sum([m[i][i] for i in range(n)]) == n:
        blink_diag_major(n)
        return True
    return False

def check_diag_minor(m,n):
    if sum([m[n-1-i][i] for i in range(n)]) == n:
        blink_diag_minor(n)
        return True
    return False

def check_vertical(m,n):
    for c in range(n): 
        if sum([m[r][c] for r in range(n)]) == n:
            blink_vertical(n, c)
            return True
    return False

def check_horizontal(m,n):
    for r in range(n): 
        if sum([m[r][c] for c in range(n)]) == n:
            blink_horizontal(n, r)
            return True
    return False

#####################################################################

def print_matrix(m,n):
	for r in range(n):
		for c in range(n):
			print('{:3d}'.format(m[r][c]), end='')
		print()
	print('\n')

#####################################################################

def create_numbers_matrix( n ):
	numbers = [ i for i in range(1,n*n+1) ]
	m = [ n*[0] for i in range(n) ]
	last_end = n*n - 1
	for r in range(n):
		for c in range(n):
			index = random.randint( 0, last_end )
			m[r][c] = numbers.pop( index )
			last_end -= 1
	return m

def create_check_matrix( n ):
	mid = int(n/2)
	m = [ n*[0] for i in range(n) ]
	m[mid][mid] = 1
	return m

def update_check_matrix( numbers_mat, check_mat, n, number ):
	for c in range(n):
		for r in range(n):
			if numbers_mat[r][c] == number:
				check_mat[r][c] = 1
				break

def update_led_matrix( check_mat, n ):
    #display.clear()
    for r in range(n):
        for c in range(n):
            display.set_pixel( c, r, 7*check_mat[r][c] )

#####################################################################

check_funcs = [check_diag_major, check_diag_minor, check_vertical, check_horizontal] 
    
while True:
    while True:
        if button_a.is_pressed(): # press button A to start 
            break
        sleep(100)

    # create a new matrix with random numbers
    numbers_m = create_numbers_matrix(N)
    # create a check matrix
    check_m = create_check_matrix(N)
    # update the LED matrix corresponding to the check matrix
    update_led_matrix( check_m, N )
    sleep(1000)
    
    bingo = False
        
    # fetch the next number
    random_numbers = [i for i in range(1,20+1)]

    for number in random_numbers:
        # check the incoming number against the number matrix
        update_check_matrix( numbers_m, check_m, N, number )
        # update the LED matrix
        update_led_matrix( check_m, N )

        # check all the bingo conditions
        for f in check_funcs:
            bingo = bingo or f( check_m, N ) 
        if bingo:
            break
        
        sleep(500) 
    
    if bingo:
        sleep(1000) 
        display.scroll( 'Bingo!', 200 )
        display.show( Image.HAPPY )
        sleep(1000) 
        bingo = False

    update_led_matrix( check_m, N )
