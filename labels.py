from lib_images import *
from lib_clustering import *
import os
import sys
import json

with open('input.json') as f:
  data = json.load(f)

# --------------------------------------------
# uncomment this block to delete all existing
# analyzed data (like from past attempts)
# --------------------------------------------
#'''
#For Linux Users:
os.system("rm %s*"%(data["shape_dir_name"]))
os.system("rm -r %s*"%(data["label_dir_name"]))
os.system("rm -r %s"%("binary"))

os.system("mkdir %s"%(data["shape_dir_name"][2:-1]))
os.system("mkdir %s"%(data["label_dir_name"]))
os.system("mkdir %s"%("binary"))
for i in range(data["num_kmeans_clusters"]):
  os.chdir(data["label_dir_name"])
  os.system("mkdir %s"%(i))
  os.chdir("..")
#'''
'''
#For Windows Users:
if (os.path.isdir(data["shape_dir_name"]) == True) and (os.path.isdir(data["label_dir_name"]) == True):
    os.system("rmdir {} /s".format(data["shape_dir_name"][2:-1]))
    os.system("rmdir {} /s".format(data["label_dir_name"][2:-1]))
    os.system("rmdir {} /s".format("binary"))

os.system("mkdir {}".format(data["shape_dir_name"][2:-1]))
os.system("mkdir {}".format(data["label_dir_name"][2:-1]))
os.system("mkdir {}".format("binary"))

os.chdir(data["label_dir_name"])
for i in range(data["num_kmeans_clusters"]):
  os.system("mkdir %s"%(i))
os.chdir("..")
'''

img_dir = data["img_dir"]
img_names = data["img_names"]
img_locs = [img_dir+name for name in img_names]
shape_dir = data["shape_dir_name"]
label_dir = data["label_dir_name"]
common_len = data["label_common_length"]
all_shapes = []
all_imgs = []

#run kmeans on the first few images and average the clusters to get the threshold value
if data["kthresh"] != 0:
    center1 = [] #darkest cluster
    center2 = [] #next darkest cluster
    total = 10
    for loc in img_locs[:total]:
        img = Image(loc)
        min_center = min(img.center)[0]
        min2_center = min(img.center[img.center != min(img.center)])
        print(img.center)
        print(min_center)
        print(min2_center)
        center1.append(min_center)
        center2.append(min2_center)
    center1 = np.median(center1)
    center2 = np.median(center2)
    #thresh_val = (center1 + center2)/2
    thresh_val = center2
    print(thresh_val)
    data["pixel_threshold"] = thresh_val
    data["kthresh"] = 0         
    with open('input.json','w') as f:
        json.dump(data,f,indent=4)

with open('input.json') as f:
  data = json.load(f)

for loc in img_locs:
    img = Image(loc)
    all_imgs.append(img)
    all_shapes = np.concatenate((all_shapes,img.big_shapes))
    img.splitShapes(shape_dir)

ret,label,center = kmeans(all_shapes,data["num_kmeans_clusters"])

for img in all_imgs:
    img.writeLabels(label_dir)
    img.drawLabels()
    write(img.clusters_image,"./clusters/"+img.location[7:-4]+".jpg")
