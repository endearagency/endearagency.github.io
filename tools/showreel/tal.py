from PIL import Image, ImageDraw
import numpy as np, sys
R='/home/claude/endearagency.github.io/'
L=lambda i:Image.open('tal/%05d.png'%i).convert('RGB')
X0,Y0,X1,Y1=488,87,1199,632; W,H=X1-X0,Y1-Y0
# Nergal hold frame from Luna hold
luna=L(408); ref=np.asarray(luna).astype(int)
card=Image.new('RGB',(W,H),(0xE4,0xE7,0xF0))
n=Image.open(R+'talent-nergal.webp').convert('RGBA')
sc=W/n.width; n=n.resize((W,round(n.height*sc)),Image.LANCZOS)
c2=card.convert('RGBA'); c2.alpha_composite(n,(0,0)); card=np.asarray(c2.convert('RGB')).astype(int)
inner=ref[Y0:Y1,X0:X1]
# rounded-corner mask: keep luna pixels that look like border/outside
m=Image.new('L',(W,H),0); ImageDraw.Draw(m).rounded_rectangle((0,0,W-1,H-1),radius=int(sys.argv[1]) if len(sys.argv)>1 else 12,fill=255)
m=np.asarray(m)[...,None]/255.
out=card*m+inner*(1-m)
# pill
bg=np.array([237,229,250]); bg=np.median(inner[60:120,520:560].reshape(-1,3),0)
pr=inner[5:55,590:711]; pm=(np.abs(pr-bg).sum(2)>18)[...,None]
out[5:55,590:711]=np.where(pm,pr,out[5:55,590:711])
nf=ref.copy(); nf[Y0:Y1,X0:X1]=out
Image.fromarray(nf.astype(np.uint8)).save('nergal_hold.png')
holds={'C':L(360),'N':Image.open('nergal_hold.png'),'Lu':L(408),'D':L(377),'E':L(393),'G':L(423)}
XB=[456,671,838,975,1083,1143,1180,1199,1206]
seq=[(352,'C','N'),(367,'N','Lu'),(382,'Lu','D'),(397,'D','E'),(412,'E','G')]
yy,xx=np.mgrid[0:720,0:1280]
for t in range(352,427):
  # current transition
  s,o,nw=[q for q in seq if q[0]<=t][-1]; k=t-s
  base=np.asarray(L(t)).astype(int).copy()
  hn=np.asarray(holds[nw]).astype(int); ho=np.asarray(holds[o]).astype(int)
  reg=(slice(70,650),slice(440,1280))
  base[reg]=hn[reg]
  if k<len(XB):
    xl=XB[k]+0.34*(639-yy)
    right=(xx>xl)
    sel=right.copy(); sel[:Y0]=0; sel[Y1:]=0; sel[:,:X0]=0; sel[:,X1:]=0
    base[sel]=ho[sel]
    im=Image.fromarray(base.astype(np.uint8)); d=ImageDraw.Draw(im)
    d.line([(XB[k]+0.34*559,80),(XB[k],639)],fill=(215,40,100),width=3)
  else: im=Image.fromarray(base.astype(np.uint8))
  im.save('tout/%05d.png'%t)
