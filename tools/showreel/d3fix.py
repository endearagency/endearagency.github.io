from PIL import Image;import numpy as np
from scipy import ndimage as nd
for f in range(2763,2914):
  a=np.asarray(Image.open('d3/%05d.png'%f).convert('RGB')).copy()
  X=432; src=a[311:441,:X].copy()
  L=a[150:446,:X].astype(int).mean(2)
  lab,n=nd.label(L<240)
  for i,sl in enumerate(nd.find_objects(lab),1):
    ys=np.nonzero(lab[sl]==i)[0]+sl[0].start
    if ys.mean()+150>243:
      y0=max(sl[0].start-2,0)+150;y1=sl[0].stop+2+150;x0=max(sl[1].start-2,0);x1=sl[1].stop+2
      m=nd.binary_dilation(lab[sl[0].start-2 if sl[0].start>=2 else 0: sl[0].stop+2, x0:x1]==i,iterations=2)
      reg=a[y0:y0+m.shape[0],x0:x0+m.shape[1]]; reg[m]=255
  z=a[241:446,:X]; z[z.astype(int).mean(2)>=200]=255
  if f>=2775: a[241:371,:X]=np.minimum(a[241:371,:X],src)
  Image.fromarray(a).save('d3o/%05d.png'%f)
