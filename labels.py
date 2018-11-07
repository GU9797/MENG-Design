from lib_images import *
from lib_clustering import *

img_dir = "/Users/kevinslater/MENG/images/"
img_names = ["jet30mpa-1.jpg"]#,"jet50mpa-1.jpg","jet100mpa-1.jpg"]
img_locs = [img_dir+name for name in img_names]
shape_dir = "./bigsplits/"
label_dir = "./labeltest/"
all_shapes = []
all_imgs = []

for loc in img_locs:
    img = Image(loc)
    all_imgs.append(img)
    all_shapes = np.concatenate((all_shapes,img.big_shapes))
    img.splitShapes(shape_dir)

ret,label,center = kmeans(all_shapes,6)

for img in all_imgs:
    img.writeLabels(label_dir)
