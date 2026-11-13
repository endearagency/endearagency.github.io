import math,sys
from PIL import Image,ImageDraw,ImageFont,ImageFilter
S=sys.argv[1]; R=sys.argv[2]
FB=S+'/fnt/package/files/poppins-latin-900-normal.woff'
GB='/usr/share/fonts/truetype/google-fonts/'
PINK=(214,51,108)
def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
# background
bg=Image.open(S+'/orig/03150.png').convert('RGB')
d=ImageDraw.Draw(bg); d.rectangle((120,215,960,620),fill=(255,255,255))
F1=ImageFont.truetype(FB,150); Fs=ImageFont.truetype(GB+'Poppins-Medium.ttf',26)
def bigtext(img,txt,x,y,fill,t):
  a=ease(t); 
  if a<=0: return
  dy=int((1-a)*40)
  lay=Image.new('RGBA',img.size,(0,0,0,0)); ld=ImageDraw.Draw(lay)
  ld.text((x+7,y+dy+8),txt,font=F1,fill=(255,255,255,0),stroke_width=2,stroke_fill=PINK+(255,))
  ld.text((x+7,y+dy+8),txt,font=F1,fill=(255,255,255,255))
  ld.text((x,y+dy),txt,font=F1,fill=fill+(255,))
  if a<1: lay.putalpha(lay.getchannel('A').point(lambda v:int(v*a)))
  img.alpha_composite(lay)
def title(i):  # i frames since start
  t=i/30
  im=bg.convert('RGBA')
  bigtext(im,'CUSTOM',148,205,(20,20,20),(t-0.0)/0.45)
  bigtext(im,'MERCH',148,352,PINK,(t-0.2)/0.45)
  d=ImageDraw.Draw(im); w=int(347*ease((t-0.5)/0.4))
  if w>0: d.rectangle((149,539,149+w,541),fill=PINK)
  a=ease((t-0.7)/0.4)
  if a>0:
    lay=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(lay).text((150,562),'Badges · Acrylic goods · Coasters · Ema',font=Fs,fill=(110,110,110,int(255*a))); im.alpha_composite(lay)
  return im.convert('RGB')
# photos
P=['merch-ema-3.webp','merch-glitter-5.webp','merch-coaster-1.webp','merch-shikishi-2.webp']
def cover(f,W,H,z,fx=.5,fy=.5):
  im=Image.open(R+'/'+f).convert('RGB'); w,h=im.size; s=max(W/w,H/h)*z
  im=im.resize((round(w*s),round(h*s)),Image.LANCZOS); x=int((im.width-W)*fx); y=int((im.height-H)*fy); return im.crop((x,y,x+W,y+H))
grad=Image.new('L',(1280,720),0); gd=ImageDraw.Draw(grad)
for y in range(720):
  v=max(0,(y-380)/340); gd.line((0,y,1280,y),fill=int(170*v**1.4))
FL=ImageFont.truetype(GB+'Poppins-Medium.ttf',14); FT=ImageFont.truetype(GB+'Poppins-Bold.ttf',46); FS=ImageFont.truetype(GB+'Poppins-Regular.ttf',18)
def label(im,t):
  a=ease(t/0.35)
  lay=Image.new('RGBA',im.size,(0,0,0,0)); ld=ImageDraw.Draw(lay); dx=int((1-a)*30)
  x=62-dx
  for ch in '04  ·  MERCH':
    ld.text((x,557),ch,font=FL,fill=(255,200,220,int(230*a))); x+=FL.getlength(ch)+4
  ld.text((60-dx,585),'Merchandise',font=FT,fill=(255,255,255,int(255*a)))
  ld.text((62-dx,646),'Badges, acrylic, coasters & more, made to your design',font=FS,fill=(255,255,255,int(235*a)))
  im.alpha_composite(lay)
cache={}
def photo(k,j,n,t):
  f=P[k]; z=1.0+0.06*(j/n)
  im=cover(f,1280,720,z).convert('RGBA')
  black=Image.new('RGBA',im.size,(0,0,0,255)); black.putalpha(grad); im.alpha_composite(black)
  label(im,t); return im.convert('RGB')
start=3059; tend=3178  # title until beat k=184 -> 105.919s -> frame 3178
end=3305
cuts=[3178,3208,3239,3269,end]
for n in range(start,end):
  if n<tend: out=title(n-start)
  else:
    k=max(i for i in range(4) if cuts[i]<=n); out=photo(k,n-cuts[k],cuts[k+1]-cuts[k],(n-tend)/30)
  if n>=3303:
    o=Image.open(S+'/orig/%05d.png'%n).convert('RGB')
    import numpy as np
    A=np.array(o).astype(int); m=((abs(A[...,0]-214)<30)&(abs(A[...,1]-51)<35)&(abs(A[...,2]-108)<35))
    B=np.array(out); B[m]=A[m]; out=Image.fromarray(B.astype('uint8'))
  out.save(S+'/fr/%05d.png'%n)
print('done')
