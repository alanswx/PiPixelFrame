#!/usr/bin/env python

import os, sys, time, math

from neopixel import *
#from fake_neopixel import *

WIDTH = 4
HEIGHT = 34
LED_COUNT      = 34*4      # Number of LED pixels.

LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 10     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


def setp(strip, x,y,c):
    if y%2 == 0:
        i = y*WIDTH+x
    else:
        i = (y+1)*WIDTH-x-1
    strip.setPixelColor(i, c)
    

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow_updown(strip, dur, num=10, dir=10, func=None):
    for n in range(num):
        for j in range(256):
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    setp(strip, x,y, wheel((j+(dir*y))%255))
            strip.show()
            if func and func(): return
            time.sleep(dur/1000.)

def rainbow_leftright(strips, dur, num=10, dir=10, func=None):
    astrip = strips[0]
    for n in range(num):
        for j in range(256):
            for strip in strips:             
                for x in range(astrip.numPixels()):
                    strip.set(x, wheel((j+(dir*x))%255))
            astrip.show()
            if func and func(): return
            time.sleep(dur/1000.)

def rainbow_center(strips, dur, num=10, dir=20, func=None):
    cx = 3.5
    cy = 3.5
   
    astrip = strips[0]

    for n in range(num):
        for j in range(256):
            n = 0
            for strip in strips:
                n = n + 1
                for x in range(strip.numPixels()):
                    dist = int(math.sqrt((cx-x)**2 + (cy-n)**2))
                    strip.set(x, wheel((j+dist*dir)%255))
            astrip.show()
            if func and func(): return
            time.sleep(dur/1000.)

# Define functions which animate LEDs in various ways.
def colorWipe(strips, color, wait_ms=50, func=None):
	"""Wipe color across display a pixel at a time."""
        astrip = strips[0]
        for i in range(astrip.numPixels()):
            for strip in strips: 
		strip.set(i, color)
            time.sleep(wait_ms/1000.)
            astrip.show()

def rainbow(strip, wait_ms=20, iterations=1, func=None):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
                if func and func(): return
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5, func=None):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel(((i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
                if func and func(): return
		time.sleep(wait_ms/1000.0)

def theaterChase(strips, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
        astrip = strips[0]
	for j in range(iterations):
		for q in range(3):
                    for strip in strips: 
			for i in range(0, strip.numPixels(), 3):
				strip.set(i+q, color)
                    astrip.show()
                    time.sleep(wait_ms/1000.0)
                    for strip in strips: 
			for i in range(0, strip.numPixels(), 3):
				strip.set(i+q, 0)
                    astrip.show()

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)


class Strip:
    def __init__(self, np, start, end, dir=True):
        self.np = np
        self.start = start
        self.end = end
        self.n = self.end - self.start
        self.dir = dir

    def show(self):
        self.np.show()
        
    def numPixels(self):
        return self.n
    
    def set(self, n, c):
        if self.dir:
            x = self.start + n
        else:
            x = self.end - n - 1
        if x < self.start or x >= self.end: return
        
        self.np.setPixelColor(x, c)
          
def main():
  nstrips = 2*8
  nleds = 34
  
  np = Adafruit_NeoPixel(nstrips*nleds, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
  np.begin()

  strips = []

  dir = True
  for i in range(nstrips):
      strip = Strip(np, nleds*i+0, nleds*i+nleds, dir)
      dir = not dir
      strips.append(strip)

  while 1:
      dur = 0
      if 1:
          colorWipe(strips, Color(255, 0, 0), dur)  # Red wipe
          colorWipe(strips, Color(0, 255, 0), dur)  # Blue wipe
          colorWipe(strips, Color(0, 0, 255), dur)  # Green wipe
          colorWipe(strips, Color(255, 255, 255), dur)  # white wipe
          colorWipe(strips, Color(127, 127, 127), dur)  # white wipe


      # Theater chase animations.
      if 1:
        theaterChase(strips, Color(127, 127, 127))  # White theater chase
        theaterChase(strips, Color(127,   0,   0))  # Red theater chase
        theaterChase(strips, Color(  0,   0, 127))  # Blue theater chase

      if 1:
        rainbow_leftright(strips, 1, dir=20)
        rainbow_leftright(strips, 1, dir=-20)
      if 1:
        rainbow_center(strips, 1, dir=20)
        rainbow_center(strips, 1, dir=-20)
      if 0:
        rainbow_updown(strip, 1, dir=20)
        rainbow_updown(strip, 1, dir=-20)

if __name__ == "__main__":
  main()
