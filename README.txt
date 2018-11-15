-----------------------------------------------------------------------------
COMMANDS
-----------------------------------------------------------------------------
python labels.py
    Preprocess image, perform kmeans clustering
-----------------------------------------------------------------------------


-----------------------------------------------------------------------------
FILES
-----------------------------------------------------------------------------
  input.json
      contains all variable values
  labels.py
      run file: parses json, preprocesses image, performs kmeans clustering
  lib_images.py
      contains definitions of Image and Shape classes
  lib_clustering.py
      contains definition of kmeans function
-----------------------------------------------------------------------------


-----------------------------------------------------------------------------
ALL INPUT DATA SHOULD BE CHANGED IN INPUT.JSON
-----------------------------------------------------------------------------
  img_dir:  directory containing input image files
  img_names:  original image file names
  shape_dir_name: directory to put all shape images
  label_dir_name: directory to put all shape images, separated by kmeans clusters
  pixel_threshold:  value above which pixels will be turned white, below which
                    will be turned black
  shape_area_pixel_minimum: minimum value of shape area, in pixels
  shape_area_pixel_maximum: maximum value of shape area, in pixels
  num_kmeans_clusters:  number of kmeans clusters
-----------------------------------------------------------------------------
