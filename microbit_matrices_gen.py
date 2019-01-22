# Author: Rawat S. (https://github.com/rsp-esl/)
# Date: 2018-09-25

from microbit import *
import random


# create a diagonal matrix
def diag_ones(n):
    return [[1 if r == c else 0 for c in range(n)] for r in range(n)]


# create a upper-triangular matrix
def upper_ones(n):
    return [[1 if r <= c else 0 for c in range(n)] for r in range(n)]


# create a lower-triangular matrix
def lower_ones(n):
    return [[1 if r >= c else 0 for c in range(n)] for r in range(n)]


# create a finish-flag matrix
def finish_flag(n):
    return [[(r + c) % 2 for c in range(n)] for r in range(n)]


# create a cross (X) matrix
def cross(n):
    return [[1 if (r == c) or (n - 1 - r == c) else 0 for c in range(n)]
            for r in range(n)]


# create a matrix with randomized elements from {0,1}
def randomize(n):
    return [[random.randint(0, 1) for c in range(n)] for r in range(n)]


# change a matrix into its corresponding transpose matrix
def transpose(m, n):
    for r in range(n):
        for c in range(r, n):
            m[r][c], m[c][r] = m[c][r], m[r][c]
    return m


# random.seed( pin0.analog_read() )

def update_leds(m, n):
    display.clear()
    for r in range(n):  # for each row
        for c in range(n):  # for each column
            display.set_pixel(c, r, 9 * (m[r][c]))


N = 5
funcs = [randomize, diag_ones, upper_ones, lower_ones, finish_flag, cross, None]
i = -1
pixels = None

while (True):
    if button_a.was_pressed():
        i = (i + 1) % len(funcs)
        if not funcs[i]:
            pixels = None
            display.clear()
        else:
            pixels = funcs[i](N)
            update_leds(pixels, N)

    if button_b.was_pressed():
        if pixels:
            transpose(pixels, N)
            update_leds(pixels, N)

    sleep(100)

################################################################
