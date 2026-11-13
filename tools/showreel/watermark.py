import sys,os,shutil,math
from PIL import Image,ImageDraw,ImageFont
O=sys.argv[1]
F=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf',10)
def wm(path):
  src=os.path.join(O,os.path.basename(path))
  if not os.path.exists(src): shutil.copy(path,src)
  im=Image.open(src).convert('RGBA'); w,h=im.size
  fs=max(22,int(min(w,h)*0.06)); f=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf',fs)
  txt='Blue Rabbit Print × endear'
  tw=int(f.getlength(txt)); D=int(math.hypot(w,h))+tw
  lay=Image.new('RGBA',(D,D),(0,0,0,0)); d=ImageDraw.Draw(lay)
  stepx=tw+fs*3; stepy=fs*4.5
  for r,y in enumerate(range(0,D,int(stepy))):
    off=(r%2)*stepx//2
    for x in range(-stepx+off,D,stepx):
      d.text((x+2,y+2),txt,font=f,fill=(0,0,0,18))
      d.text((x,y),txt,font=f,fill=(255,255,255,62))
  lay=lay.rotate(30,resample=Image.BICUBIC)
  l=(D-w)//2;t=(D-h)//2; lay=lay.crop((l,t,l+w,t+h))
  out=Image.alpha_composite(im,lay).convert('RGB'); out.save(path,quality=84,method=6)
for p in sys.argv[2:]: wm(p); print(p)
