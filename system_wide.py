import numpy as np
import cv2
import matplotlib.pyplot as plt
import json

with open('input.json') as f:
  data = json.load(f)


def plot(img):
  dims = img.shapes[0].boundary
  bounds = dims[2:4]
  r = np.arange(bounds[0]+0.5,bounds[1]+0.5,1.0)

  rbins = []
  for i in r:
    count = 0
    for j in range(len(img.shapes)-1):
      mmin = img.shapes[j+1].boundary[2]
      mmax = img.shapes[j+1].boundary[3]
      if i > mmin and i < mmax:
        count += 1
    rbins.append(count)

  binavg = []
  blocksize = 12.0
  ravg = []
  count = 0
  tempblock = 0
  for i in range(len(r)):
    if count < blocksize:
      tempblock += rbins[i]
      count += 1
    else:
      ravg.append(i-(blocksize/2.0))
      binavg.append(tempblock/blocksize)
      tempblock = rbins[i]
      count = 1

  plt.plot(ravg,binavg)
  plt.title('All shapes')
  plt.xlabel('Distance from nozzle')
  plt.ylabel('Number of shapes')
  plt.show()



def by_size(img):
  dims = img.shapes[0].boundary
  bounds = dims[2:4]
  r = np.arange(bounds[0]+0.5,bounds[1]+0.5,1.0)

  smallmax = 100.0
  medmax = 500.0
  largemax = 1000.0
  rbins_small = []
  rbins_medium = []
  rbins_large = []
  rbins_huge = []

  for i in r:
    count = 0
    scount = 0
    mcount = 0
    lcount = 0
    hcount = 0
    for j in range(len(img.shapes)-1):
      area = img.shapes[j+1].area
      #print(area)
      mmin = img.shapes[j+1].boundary[2]
      mmax = img.shapes[j+1].boundary[3]
      if i > mmin and i < mmax:
        if area < smallmax:
          scount += 1
        if area < medmax and area > smallmax:
          mcount += 1
        if area < largemax and area > medmax:
          lcount += 1
        if area > largemax:
          hcount += 1
    rbins_small.append(scount)
    rbins_medium.append(mcount)
    rbins_large.append(lcount)
    rbins_huge.append(hcount)

  sbinavg = []
  mbinavg = []
  lbinavg = []
  hbinavg = []

  blocksize = 75.0
  ravg = []
  count = 0

  stempblock = 0
  mtempblock = 0
  ltempblock = 0
  htempblock = 0

  for i in range(len(r)):
    if count < blocksize:
      stempblock += rbins_small[i]
      mtempblock += rbins_medium[i]
      ltempblock += rbins_large[i]
      htempblock += rbins_huge[i]
      count += 1
    else:
      ravg.append(i-(blocksize/2.0))
      sbinavg.append(stempblock/blocksize)
      mbinavg.append(mtempblock/blocksize)
      lbinavg.append(ltempblock/blocksize)
      hbinavg.append(htempblock/blocksize)
      stempblock = rbins_small[i]
      mtempblock = rbins_medium[i]
      ltempblock = rbins_large[i]
      htempblock = rbins_huge[i]
      count = 1

  plt.plot(ravg,sbinavg,label='small',color='cyan',linewidth=2.0)
  plt.plot(ravg,mbinavg,label='medium',color='blue',linewidth=2.0)
  plt.plot(ravg,lbinavg,label='large',color='grey',linewidth=2.0)
  plt.plot(ravg,hbinavg,label='huge',color='black',linewidth=2.0)

  plt.legend()
  plt.title('shapes by size')
  plt.xlabel('Distance from nozzle')
  plt.ylabel('Number of shapes')
  plt.show()
