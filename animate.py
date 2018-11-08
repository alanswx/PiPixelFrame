#! /usr/bin/env python

"""python program to solve the world problems..."""

import os, sys, string, time, logging, argparse

_version = "0.1"

#from neopixel import *
from fake_neopixel import *

# apt-get install python-imaging

from PIL import Image, ImageSequence

LED_COUNT      = 64      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

def start(files):
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
  strip.begin()

  fn = files[0]

  path,fname = os.path.split(fn)

  im = Image.open(fn)

  dur = im.info['duration']

  frames = [frame.copy() for frame in ImageSequence.Iterator(im)]

  frames8 = []

  for frame in frames:
      frame = frame.convert('RGB')
      if fname == "heart.gif":
          frame = frame.crop((50,50,450,450))
          frame = frame.resize((8,8))

      elif fname == "lemming.gif":
          frame = frame.crop((28,16,60,60))
          frame = frame.resize((8,8), Image.BICUBIC)
      else:
          frame = frame.resize((8,8), Image.BICUBIC)

      frames8.append(frame)

  while 1:
      for frame in frames8:
          for y in range(frame.size[1]):
              for x in range(frame.size[0]):
                  r,g,b = frame.getpixel((x,y))
                  if y%2 == 0:
                      i = y*8+x
                  else:
                      i = (y+1)*8-x-1
                  strip.setPixelColor(i, Color(g,r,b))
          strip.show()
          time.sleep(dur/1000.)

def test():
  logging.warn("Testing")

def parse_args(argv):
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description=__doc__)

  parser.add_argument("-t", "--test", dest="test_flag", 
                    default=False,
                    action="store_true",
                    help="Run test function")
  parser.add_argument("--log-level", type=str,
                      choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                      help="Desired console log level")
  parser.add_argument("-d", "--debug", dest="log_level", action="store_const",
                      const="DEBUG",
                      help="Activate debugging")
  parser.add_argument("-q", "--quiet", dest="log_level", action="store_const",
                      const="CRITICAL",
                      help="Quite mode")
  parser.add_argument("files", type=str, nargs='+')

  args = parser.parse_args(argv[1:])

  return parser, args

def main(argv, stdout, environ):
  if sys.version_info < (3, 0): reload(sys); sys.setdefaultencoding('utf8')

  parser, args = parse_args(argv)

  logging.basicConfig(format="[%(asctime)s] %(levelname)-8s %(message)s", 
                    datefmt="%m/%d %H:%M:%S", level=args.log_level)

  if args.test_flag:  test();   return

  start(args.files)

if __name__ == "__main__":
  main(sys.argv, sys.stdout, os.environ)
