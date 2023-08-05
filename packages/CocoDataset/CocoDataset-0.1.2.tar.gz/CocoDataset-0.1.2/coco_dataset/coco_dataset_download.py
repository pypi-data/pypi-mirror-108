from pycocotools.coco import COCO
import requests
import os
# instantiate COCO specifying the annotations json path
def coco_dataset_download(class_name,images_count,annotations_path):

    coco = COCO(annotations_path)
    # Specify a list of category names of interest
    catIds = coco.getCatIds(catNms=[class_name])
    # Get the corresponding image ids and images using loadImgs
    imgIds = coco.getImgIds(catIds=catIds)
    images = coco.loadImgs(imgIds)
    os.mkdir (class_name)
    # Save the images into a local folder
    count=0
    # specified count images for class name
    for im in images:
        img_data = requests.get(im['coco_url']).content
        with open('./'+ class_name +'/'+ im['file_name'], 'wb') as handler:
            handler.write(img_data)
        count+=1
        if count>images_count:
            print('finished images download')
            break
        print('no.of image:',count)   