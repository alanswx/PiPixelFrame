from PIL import Image
from neopixel import *



def animate(name):
  print('animated_gif',name)
  im = Image.open(name)
  seq=[]
  try:
    while 1:
       seq.append(im.copy())
       im.seek(len(seq))
  except EOFError:
       pass
  print('viewing images now')
  for image in seq:
      rgbim = image.convert('RGB')
      for x in range(8):
        for y in range(8):
           r,g,b=rgbim.getpixel((x,y))
           c = Color(r,g,b)
           setp(strip, x,y,c)
      strip.show()
      if func and func(): return
      print('duration',im.info['duration'])
      time.sleep(wait_ms/1000.0)

animate('gifs/policeb2.gif')
