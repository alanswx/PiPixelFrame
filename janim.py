#!/usr/bin/env python

import os, sys, time, math

import fontdemo

try:
  from neopixel import *
except ImportError:
  neopixel = None

from PIL import Image
#from fake_neopixel import *

LED_COUNT      = 64      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 128 # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

def Color(red, green, blue, white = 0):
	"""Convert the provided red, green, blue color to a 24-bit color value.
	Each color component should be a value 0-255 where 0 is the lowest intensity
	and 255 is the highest intensity.
	"""
	return (white << 24) | (green << 16)| (red << 8) | blue

def setp(strip, x,y,c):
    x=7-x
    if y%2 == 0:
        i = y*8+x
    else:
        i = (y+1)*8-x-1
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
            for y in range(8):
                for x in range(8):
                    setp(strip, x,y, wheel((j+(dir*y))%255))
            strip.show()
            if func and func(): return
            time.sleep(dur/1000.)

def rainbow_leftright(strip, dur, num=10, dir=10, func=None):
    for n in range(num):
        for j in range(256):
            for y in range(8):
                for x in range(8):
                    setp(strip, x,y, wheel((j+(dir*x))%255))
            strip.show()
            if func and func(): return
            time.sleep(dur/1000.)

def rainbow_center(strip, dur, num=10, dir=20, func=None):
    cx = 3.5
    cy = 3.5
    for n in range(num):
        for j in range(256):
            for y in range(8):
                for x in range(8):
                    dist = int(math.sqrt((cx-x)**2 + (cy-y)**2))
                    setp(strip, x,y, wheel((j+dist*dir)%255))
            strip.show()
            if func and func(): return
            time.sleep(dur/1000.)

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50, func=None):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
                if func and func(): return
		time.sleep(wait_ms/1000.0)

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

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

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

def scroll_text(strip, txt, wait_ms=100, textcolor=(255,255,255),func=None):
  fnt = fontdemo.Font('helvetica.ttf', 11)
  txt = fnt.render_text('  ' + txt +'  ', 14, 8)

  for x in range(txt.width):
    for y in range(8):
      for x2 in range(8):
        c = Color(0,0,0)
        if x2+x < txt.width: 
          if txt.pixels[(y*txt.width)+(x+x2)]:
            c = Color(textcolor[0],textcolor[1],textcolor[2]) #Color(255,255,255)
        setp(strip, x2,y,c)
    strip.show()
    if func and func(): return
    time.sleep(wait_ms/1000.0)

def animated_gif(strip, name,wait_ms=500,func=None,repeat=1):
 try:
  print('animated_gif',name)
  im = Image.open(name)
  seq=[]
  if True:
   try:
    while 1:
       seq.append((im.copy(),im.info['duration']))
       im.seek(len(seq))
   except EOFError:
       pass
   if (len(seq)==1):
      wait_ms=1500
   print('viewing images now')
   for count in range(repeat):
    for image,duration in seq:
      rgbim = image.convert('RGB')
      for x in range(8):
        for y in range(8):
           r,g,b=rgbim.getpixel((x,y))
           c = Color(r,g,b)
           setp(strip, x,y,c)
      strip.show()
      print('duration',im.info['duration'])
      if (duration==0):
         duration=wait_ms
      print(duration)
      if func and func(): return
      time.sleep(duration/1000.0)
 except Exception as e:
       print('GIF Exception',e)
       pass
          
def main():    
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
  strip.begin()

  while 1:
      animated_gif(strip, 'gifs/Hi.gif')
      #animated_gif(strip, 'gifs/policeb2.gif')
      #animated_gif(strip, 'gifs/flappy.gif')
      #animated_gif(strip, 'gifs/mario2.gif')
      #animated_gif(strip, 'gifs/pacman.gif')
      #animated_gif(strip, 'gifs/Lemming_animation.gif')
      #scroll_text(strip, 'Hello Jamie')

      colorWipe(strip, Color(255, 0, 0))  # Red wipe
      if 1:
        colorWipe(strip, Color(0, 255, 0))  # Blue wipe
        colorWipe(strip, Color(0, 0, 255))  # Green wipe
      # Theater chase animations.
      if 0:
        theaterChase(strip, Color(127, 127, 127))  # White theater chase
        theaterChase(strip, Color(127,   0,   0))  # Red theater chase
        theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
      # Rainbow animations.
      if 0:
        rainbow(strip)
        rainbowCycle(strip)
        theaterChaseRainbow(strip)

      #rainbow_leftright(strip, 1, dir=20)
      #rainbow_leftright(strip, 1, dir=20)
      #rainbow_leftright(strip, 1, dir=-20)
      #rainbow_center(strip, 1, dir=20)
      #rainbow_center(strip, 1, dir=-20)
      #rainbow_updown(strip, 1, dir=20)
      #rainbow_updown(strip, 1, dir=-20)

if __name__ == "__main__":
  main()
