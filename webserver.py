#! /usr/bin/env python

"""python program to solve the world problems..."""

import os, sys, string, time, logging, argparse

import subprocess

_version = "0.1"

import bottle
import json
import base64
import ipaddr
import glob

import janim
import threading

import csv

#import fake_neopixel
try:
  import neopixel
except ImportError:
  neopixel = None


LED_COUNT      = 64      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
#LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

app = bottle.Bottle()
app.strip = None
app.wlan0_ip = None

def clear_display(strip):
  if not strip: return
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, 0)
  strip.show()

def setp(strip,x,y,c):
  if not strip: return
  if y%2 == 0:
    i = y*8+x
  else:
    i = (y+1)*8-x-1
  strip.setPixelColor(i, c)


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()
        self.daemon = True

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

class DisplayGifThread(StoppableThread):
  def __init__(self,strip,filename):
    super(DisplayGifThread, self).__init__()
    
    self.strip = strip
    self.filename = filename

  def run(self):
    janim.animated_gif(self.strip, self.filename, func=self.stopped) 

class DisplayTextThread(StoppableThread):
  def __init__(self, strip, text):
    super(DisplayTextThread, self).__init__()
    
    self.strip = strip
    self.text = text

  def run(self):
    while not self.stopped():
      janim.scroll_text(self.strip, self.text, func=self.stopped)

class DisplayJAnimThread(StoppableThread):
  def __init__(self, strip):
    super(DisplayJAnimThread, self).__init__()
    
    self.strip = strip

  def run(self):
    while not self.stopped():
      janim.colorWipe(self.strip, neopixel.Color(255, 0, 0), func=self.stopped)  # Red wipe
      janim.colorWipe(self.strip, neopixel.Color(0, 255, 0), func=self.stopped)  # Blue wipe
      janim.colorWipe(self.strip, neopixel.Color(0, 0, 255), func=self.stopped)  # Green wipe

      if 1:
        janim.rainbow_leftright(self.strip, 1, dir=20, func=self.stopped)
        janim.rainbow_leftright(self.strip, 1, dir=20, func=self.stopped)
        janim.rainbow_leftright(self.strip, 1, dir=-20, func=self.stopped)
        janim.rainbow_center(self.strip, 1, dir=20, func=self.stopped)
        janim.rainbow_center(self.strip, 1, dir=-20, func=self.stopped)
        janim.rainbow_updown(self.strip, 1, dir=20, func=self.stopped)
        janim.rainbow_updown(self.strip, 1, dir=-20, func=self.stopped)

def playlistloader(name):
  column_names=[]
  playlists=[]
  with open(name, 'rb') as csvfile:
     csvreader= csv.reader(csvfile)
     line=0
     for row in csvreader:
         if not len(column_names):
            for col in row:
              column_names.append(col)
         else:
            cur = {}
            i=0
            cur['number']=line
            line=line+1
            for col in row:
              cur[column_names[i]]=col
              i=i+1
            playlists.append(cur)
     print(playlists)
  return playlists
  
class DisplayShowPlaylistThread(StoppableThread):
  def __init__(self, strip,playlist):
    super(DisplayShowPlaylistThread, self).__init__()
    # load the playlist
    self.playlist=playlistloader(playlist)
    self.strip = strip

  def run(self):
    print('DisplayShowPlaylistThread - run')
    print(self.playlist)
    while not self.stopped():
       for entry in self.playlist:
          print('entry:',entry)
          if (entry['type']=='image'):
              # play a gif here
              janim.animated_gif(self.strip, entry['name'], func=self.stopped) 
          elif (entry['type']=='colorwipe'):
              janim.colorWipe(self.strip, neopixel.Color(255, 0, 0), func=self.stopped)  # Red wipe
          elif (entry['type']=='rainbow'):
              janim.rainbow_leftright(self.strip, 1, dir=20, func=self.stopped)
          elif (entry['type']=='text'):
              janim.scroll_text(self.strip, entry['name'], func=self.stopped)

  

@app.route('/')
@app.route('/index.html')
def index():
  if app.wlan0_ip:
    if bottle.request.headers.get('Host') != app.wlan0_ip:
      bottle.redirect("http://%s/index.html" % app.wlan0_ip)

  return bottle.template("index")

@app.route('/client_mode')
def client_mode():
  #app.displayThread.stop()

  #subprocess.call(["./start_wifi"])

  #app.wlan0_ip = ipaddr.get_ip('wlan0')

  #app.displayThread = DisplayTextThread(app.strip, '%s' % app.wlan0_ip)
  #app.displayThread.start()
  
  bottle.redirect("/index.html")

@app.route('/ap_mode')
def ap_mode():
  #app.displayThread.stop()

  #subprocess.call(["./start_ap"])
  #app.wlan0_ip = ipaddr.get_ip('wlan0')

  #app.displayThread = DisplayTextThread(app.strip, 'AP')
  #app.displayThread.start()
  bottle.redirect("/index.html")

@app.route('/gallery')
def gallery():
  animations = []
  files = glob.glob("gallery/*.meta")
  for fn in files:
    anim = json.load(open(fn, "r"))
    animations.append(anim)
  return bottle.template("gallery", animations=animations)


@app.route("/gifs/<filepath:re:.*\.(gif)>")
def img(filepath):
  return bottle.static_file(filepath,root="gifs")

@app.route("/showgif/gifs/<filepath:re:.*\.(gif)>")
def showgif(filepath):
  if neopixel:
     app.displayThread.stop()
     app.displayThread = DisplayGifThread(app.strip, 'gifs/'+filepath)
     app.displayThread.start()
  return "showgif:"+filepath

@app.route("/playlists/<filepath:re:.*\.(csv)>")
def showplaylist(filepath):
  playlists= []
  print(filepath)
  playlists = playlistloader('playlists/'+filepath)
  print(playlists)
  return bottle.template("playlist", playlist=playlists)

@app.route("/playlists/")
def showplaylists():
  playlists= []
  files = glob.glob("playlists/*.csv")
  for fn in files:
    playlists.append({'name':fn})
  return bottle.template("playlist_gallery", playlists=playlists)


@app.route("/playshow/<filepath:re:.*\.(csv)>")
def displayplaylist(filepath):
  if neopixel:
     app.displayThread.stop()
     app.displayThread = DisplayShowPlaylistThread(app.strip, filepath)
     app.displayThread.start()
  else:
     a = DisplayShowPlaylistThread(app.strip, filepath)
  return "showplaylist:"+filepath


@app.route('/gifgallery')
def gallery():
  animations = []
  files = glob.glob("gifs/*.gif")
  for fn in files:
    animations.append({'name':fn})
  return bottle.template("gif_gallery", animations=animations)

@app.route('/gallery/<filename>')
def piskel(filename):
  app.displayThread.stop()

  fn = os.path.join("gallery", "%s.meta" % filename)
  anim = json.load(open(fn, "r"))
  afn = os.path.join("gallery", "%s.piskel" % filename)
  piskel = open(afn, "r").read()

  if anim['public'] is None:
    anim['public'] = 'false'

  initsection = bottle.template("piskel", anim=anim, piskel=piskel)

  body = open("piskel/index.html").read()

  body = body.replace("<!-- piskel init here -->", initsection)

  return body

@app.route('/piskel/<filename:path>', name='static')
def piskel(filename):
  app.displayThread.stop()
  return bottle.static_file(filename, root="piskel")

@app.route('/setpixel')
def setpixel():
  x = int(bottle.request.query.get('x'))
  y = int(bottle.request.query.get('y'))
  r = int(bottle.request.query.get('r'))
  g = int(bottle.request.query.get('g'))
  b = int(bottle.request.query.get('b'))

  if app.strip:
    setp(app.strip, x,y,neopixel.Color(g,r,b))
    app.strip.show()
  
  return "setpixel"

@app.route('/setpixels', method="POST")
def setpixels():
  width = int(bottle.request.forms.get('width', '0'))
  height = int(bottle.request.forms.get('height', '0'))
  pixels = bottle.request.forms.get('pixels', '')

  if not pixels: return "None"
  
  for y in range(height):
    for x in range(width):
      i = (y*width + x)*6
      c = pixels[i:i+6]

      r = string.atoi(c[0:2], 16)
      g = string.atoi(c[2:4], 16)
      b = string.atoi(c[4:6], 16)

      if app.strip:
        setp(app.strip, x,y,neopixel.Color(g,r,b))

  if app.strip:
    app.strip.show()

  return "setpixels"

@app.route('/piskelsave', method="POST")
def piskelsave():
  print (bottle.request.forms.items())

  name = bottle.request.forms.get('name')
  framesheet = bottle.request.forms.get('framesheet')
  framesheet_as_png = bottle.request.forms.get('framesheet_as_png')
  fps = bottle.request.forms.get('fps')
  frames = bottle.request.forms.get('frames')
  public = bottle.request.forms.get('public')
  description = bottle.request.forms.get('description')
  
  d = {}
  d['description'] = description
  d['public'] = public
  d['frames'] = frames
  d['fps'] = fps
  d['name'] = name
  d['png'] = framesheet_as_png

  open(os.path.join("gallery", name + ".piskel"), "w").write(framesheet)
  open(os.path.join("gallery", name + ".meta"), "w").write(json.dumps(d))
  if 1:
    if framesheet_as_png.startswith("data:image/png;base64,"):
      framesheet_as_png = framesheet_as_png[len("data:image/png;base64,"):]
      framesheet_as_png = base64.decodestring(framesheet_as_png)
  open(os.path.join("gallery", name + ".png"), "w").write(framesheet_as_png)

  return "pixelsave"

@app.route('/piskelupload', method="POST")
def piskelupload():
  print (bottle.request.forms.items())
  return "pixelupload"

## @app.route('/<path:re:.*>')
## def catchall(path):
##   if app.wlan0_ip:
##     if bottle.request.headers.get('Host') != app.wlan0_ip:
##       bottle.redirect("http://%s/index.html" % app.wlan0_ip)
##   bottle.abort(404, "File not found")

def start():
  if neopixel:
    app.strip = neopixel.Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    app.strip.begin()
    clear_display(app.strip)

    #app.displayThread = DisplayJAnimThread(app.strip)
    app.displayThread = DisplayShowPlaylistThread(app.strip,'playlists/imageloop.csv')
    app.displayThread.start()
  else:
    app.strip = None
    
  app.wlan0_ip = ipaddr.get_ip('wlan0')
  app.run(host='0.0.0.0', port=80, debug=True)

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
  #parser.add_argument("files", type=str, nargs='+')

  args = parser.parse_args(argv[1:])

  return parser, args

def main(argv, stdout, environ):
  if sys.version_info < (3, 0): reload(sys); sys.setdefaultencoding('utf8')

  parser, args = parse_args(argv)

  logging.basicConfig(format="[%(asctime)s] %(levelname)-8s %(message)s", 
                    datefmt="%m/%d %H:%M:%S", level=args.log_level)

  if args.test_flag:  test();   return

  start()

if __name__ == "__main__":
  main(sys.argv, sys.stdout, os.environ)
