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
'''
#For Linux Users:
os.system("rm %s*"%(data["shape_dir_name"]))
os.system("rm -r %s*"%(data["label_dir_name"]))
for i in range(data["num_kmeans_clusters"]):
  os.chdir(data["label_dir_name"])
  os.system("mkdir %s"%(i))
  os.chdir("..")
'''
#'''
#For Windows Users:
if (os.path.isdir(data["shape_dir_name"]) == True) and (os.path.isdir(data["label_dir_name"]) == True):
    os.system("rmdir {} /s".format(data["shape_dir_name"][2:-1]))
    os.system("rmdir {} /s".format(data["label_dir_name"][2:-1]))

os.system("mkdir {}".format(data["shape_dir_name"][2:-1]))
os.system("mkdir {}".format(data["label_dir_name"][2:-1]))

os.chdir(data["label_dir_name"])
for i in range(data["num_kmeans_clusters"]):
  os.system("mkdir %s"%(i))
os.chdir("..")
#'''

img_dir = data["img_dir"]
img_names = data["img_names"]
img_locs = [img_dir+name for name in img_names]
shape_dir = data["shape_dir_name"]
label_dir = data["label_dir_name"]
all_shapes = []
all_imgs = []

for loc in img_locs:
    img = Image(loc)
    all_imgs.append(img)
    all_shapes = np.concatenate((all_shapes,img.big_shapes))
    img.splitShapes(shape_dir)

ret,label,center = kmeans(all_shapes,data["num_kmeans_clusters"])

for img in all_imgs:
    img.writeLabels(label_dir)
