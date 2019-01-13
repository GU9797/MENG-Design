-----------------------------------------------------------------------------
PAST COMMIT, NEXT STEPS
-----------------------------------------------------------------------------
done on last commit:
- print all binary images to new directory
- reconfigured automated shape labeling

done on second to last commit:
- rotate image
    - Prints out shapes with direction of acceleration along horizontal
      (just generally easier to visualize)
    - I did this arbitrarily, since the nozzle is in the same place for all
      our images.  We probably want to use edge to detection to generalize
      this eventually
        - arbitrary angle is at top of lib_images.py, if you want to change it
- added write_json.py
    - So you don't have to write out all the file names in the image directory
    - CHANGE INPUT VALUES HERE
   
In my opinion, logical next steps:
- Separate by size before applying kmeans
- kmeans elbow method?
- adaptive thresholding, or some other method of separating 'big shapes'
-----------------------------------------------------------------------------


-----------------------------------------------------------------------------
COMMANDS
-----------------------------------------------------------------------------
python write_json.py
    write json file used by labels.py

python labels.py
    Preprocess image, perform kmeans clustering
-----------------------------------------------------------------------------


-----------------------------------------------------------------------------
FILES
-----------------------------------------------------------------------------
  write_json.py
      writes input.json; ideally the only front-end file
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
ALL INPUT DATA SHOULD BE CHANGED IN WRITE_JSON.PY (which prints input.json)
-----------------------------------------------------------------------------
  img_dir:  directory containing input image files
  label_common_length:  number of characters conserved at beginning of all image
                    labels, chopped off at beginning of shape label 
  img_names:  original image file names
  shape_dir_name: directory to put all shape images
  label_dir_name: directory to put all shape images, separated by kmeans clusters
  pixel_threshold:  value above which pixels will be turned white, below which
                    will be turned black
  shape_area_pixel_minimum: minimum value of shape area, in pixels
  shape_area_pixel_maximum: maximum value of shape area, in pixels
  num_kmeans_clusters:  number of kmeans clusters
  Otsu: 1 for Otsu thresholding, any other number for manual thresholding
-----------------------------------------------------------------------------
