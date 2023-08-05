# COCO Dataset Download
This is a Python package for easy to download Determining Specific Part of CoCo Dataset
for any class name  and any a count images 

## Installation
```
pip install CocoDataset==0.1.2
or in colab google cloud
!pip install CocoDataset==0.1.2

```
## Tutorial

```
[source](https://colab.research.google.com/drive/1QuLLsvX-DnOcOVWxcKWglIzDnxV_OHxE?usp=sharing)

u can see tutorial in colab google drive

```
# Usage
## get images for specified class name

```
from coco_dataset import coco_dataset_download as cocod
class_name='person'  #class name 
images_count=50       #count of images  
annotations_path='/content/annotations/instances_train2014.json' #path of coco dataset annotations 
#call download function
cocod.coco_dataset_download(class_name,images_count,annotations_path)
``` 

