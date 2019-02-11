import cv2
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------
#normalize one directory at a time
location = "./Honda/80bar/T2-X=0.00_Y=1.00__"

#which images in the directory do we want to normalize?
start = 4
stop = 399

#do we want to save the rescaled images, and if so where?
write = 1
output = "./Honda/80bar_rescaled/"

#number of frames to average when calculating the background,
#you can change this for each set of spray images
background_frames = 8
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#calculate background
imgs = []
for n in range(start,background_frames+start):

    if n<10:
        num = "000"+str(n)
    else:
        num = "00"+str(n)

    img = cv2.imread(location+num+".tif", -1) #if we don't set -1 it will read as 8 bit
    img = img[75:,:] #cut out nozzle from frame
# uncomment to show images
#    plt.imshow(img)
#    plt.show()
    imgs.append(img)

bg = np.mean(imgs,axis=0)
# uncomment to show background subtracted
#plt.imshow(bg,cmap='gray')
#plt.imshow(bg)
plt.show()
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#subtract the background from each images,
#then calculate the overall max/min pixel values.
#These max/min values must be consistent across all sets of images we want to analyze!
#Need to keep this in mind when normalizing multiple directories
imgs_nobg = []
max_pixel = -1
min_pixel = np.inf

print("Subtracting background...")

for n in range(start, stop+1):

    if n<10:
        num = "000"+str(n)
    elif n<100:
        num = "00"+str(n)
    else:
        num = "0"+str(n)
    
    img = cv2.imread(location+num+".tif",-1)
    img = img[75:,:]
    img_nobg = img - bg

    imgs_nobg.append(img_nobg)
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
# ensure background is the same average pixel value for each frame
# background of image will be set to 0 (before rescaling)
imgs_nobg2 = []
bgs = []

for n in range(len(imgs_nobg)):
    img = imgs_nobg[n]
# choose which section of the image to define as the background
    bg = img[:,:100]  # entire left side
#    bg = img[:100,:100]  # top right corner
#    bg = img[200:300,:100] # middle of left side
    bg_pixel = np.mean(bg)
    bgs.append(bg_pixel)
    img_nobg2 = img - bg_pixel

    img_max = img_nobg2.max()
    img_min = img_nobg2.min()
    if img_max>max_pixel:
        max_pixel = img_max
    if img_min<min_pixel:
        min_pixel = img_min

    imgs_nobg2.append(img_nobg2)

bgs = np.array(bgs)
# uncomment to plot histogram of values subtracted from background
# (shows spread of difference in background values across all images before normalization)
#grey_histo = np.histogram(bgs, int(bgs.max() - bgs.min()),density=True)
#plt.bar(grey_histo[1][1:],grey_histo[0])
#plt.xlabel('pixel value')
#plt.ylabel('percent of images')
#plt.show()
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#now rescale each image to 8-bit range
#pixel values will still be stored as floats
imgs_rescaled = []

print("Rescaling images...")

for img in imgs_nobg2:
    img_rescaled = 255*((img-min_pixel)/(max_pixel-min_pixel))
    imgs_rescaled.append(img_rescaled)

#write images -- this will automatically convert all values to uint8
for i in range(len(imgs_rescaled)):
  cv2.imwrite(output+str(i)+".tif",imgs_rescaled[i])
