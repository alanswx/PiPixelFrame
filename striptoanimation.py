from PIL import Image,ImageDraw

im = Image.open("try2.png")
newim = Image.new("RGBA",(8,8))
width,height = im.size
num=0
x=0
images=[]
while x< width-8:
  x=x+2
  draw = ImageDraw.Draw(newim)
  draw.rectangle(((0, 0), (8, 8)), outline="#ffffffff",fill="#FFFFFFFF")
  newim.paste(im,(x*-1,0))
  num=num+1
  name='output/new_'+"{:03d}".format(num)+'.gif'
  print(name)
  images.append(newim.copy())
  newim.save(name,transparency=0)

images[0].save('anitest.gif',
               save_all=True,
               append_images=images[1:],
               duration=200,transparency=0,
               loop=0)
