import cv2
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------
#normalize one directory at a time
location = "../Hole1/80bar/T1/SE_T1-X=0.00_Y=0.00__"

#which images in the directory do we want to normalize?
start = 1
stop = 49

#do we want to save the rescaled images, and if so where?
write = 1
output = "../Hole1/80bar/T1_normalized/"

#number of frames to average when calculating the background,
#you can change this for each set of spray images
background_frames = 30
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#calculate background
imgs = []
nozzle_imgs = []
for n in range(start,background_frames+start):

    if n<10:
        num = "000"+str(n)
    else:
        num = "00"+str(n)

    img = cv2.imread(location+num+".tif", -1) #if we don't set -1 it will read as 8 bit

    #set a portion of the nozzle to zero;ie don't subtract the background here
    nozzle_imgs.append(img[:100,:250])
    cropped_img = np.copy(img)
    #uncomment for 2-point normalization
    for j in range(100):
        for i in range(250):
            cropped_img[j][i] = 0

# uncomment to show images
#    plt.imshow(img)
#    plt.show()

    imgs.append(cropped_img)

bg = np.mean(imgs,axis=0)
nozzle_bg = np.mean(np.mean(nozzle_imgs,axis=0)) #mean value of nozzle across bg frames
bg_rescaled = 255*((bg-np.min(bg))/(np.max(bg)-np.min(bg)))
cv2.imwrite(output+"background.png",bg_rescaled)
# uncomment to show background subtracted
#plt.imshow(bg,cmap='gray')
#plt.imshow(bg)
#plt.show()
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
    img_nobg = img - bg

    imgs_nobg.append(img_nobg)
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
# ensure background is the same average pixel value for each frame
# background of image will be set to 0 (before rescaling)
imgs_nobg2 = []
bgs = []

print("Normalizing images...")

for n in range(len(imgs_nobg)):
    img = imgs_nobg[n]
# choose which section of the image to define as the background
    bg = img[:,700:]  # entire right side
    bg_pixel = np.mean(bg)
    nozzle = img[:100,:250]
    nozzle_pixel = np.mean(nozzle)
    bgs.append(bg_pixel)

    #one-point normalization
    #img_nobg2 = img - bg_pixel

    #two-point normalization
    img_nobg2 = (img - bg_pixel)*(nozzle_bg/(nozzle_pixel-bg_pixel))

    #calculate global max and min for 8-bit rescaling
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

print("Rescaling to 8-bit...")

for img in imgs_nobg2:
    img_rescaled = 255*((img-min_pixel)/(max_pixel-min_pixel))
    imgs_rescaled.append(img_rescaled)

#write images -- this will automatically convert all values to uint8
for i in range(len(imgs_rescaled)):
  cv2.imwrite(output+str(i)+".tif",imgs_rescaled[i])

#plot normalized pixel distributions for each image
plt.figure(num=None,figsize=(12,9),dpi=80,facecolor="w",edgecolor = "k")
for img in imgs_rescaled[34:]:
    spray = img[180:,:]
    g = spray.flatten()
    hist = np.histogram(g,int(g.max()-g.min()),density=True)
    plt.plot(hist[1][1:],hist[0])
plt.xlim([42,50])
plt.title("Pixel values of 1-point normalized spray images")
#plt.savefig(output+"hist_1xnormed_zoom.png")
