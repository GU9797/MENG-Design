import os

dir_name = "images/"
thresh = 80  #pixel_threshold
sapmin = 10  #shape_area_pixel_minimum
sapmax = 400 #shape_area_pixel_maximum
ssrm = 3.45  #shape_side_ratio_maximum
nkc = 20     #num_kmeans_clusters

num_files = len(os.listdir("./" + dir_name))

with open("input.json",'w') as l:
  l.write('{\n\t"comment" : "see README for descriptions",\n')
  l.write('\t"img_dir" : "' + dir_name + '",\n')
  l.write('\t"img_names": [\n')
  n = 1
  for f in os.listdir("./" + dir_name):
    if n < num_files:
      l.write('\t\t"' + f + '",\n')
      n += 1
    else:
      l.write('\t\t"' + f + '"\n')
  l.write('\t\t],\n')
  l.write('\t"shape_dir_name" : "./bigsplits/",\n')
  l.write('\t"label_dir_name" : "./labeltest/",\n')
  l.write('\t"pixel_threshold": ' + str(thresh) + ',\n')
  l.write('\t"shape_area_pixel_minimum": ' + str(sapmin) + ',\n')
  l.write('\t"shape_area_pixel_maximum": ' + str(sapmax) + ',\n')
  l.write('\t"shape_side_ratio_maximum": ' + str(ssrm) + ',\n')
  l.write('\t"num_kmeans_clusters": ' + str(nkc) + ',\n')
  l.write('\t"Otsu": 0\n')
  l.write('}')
