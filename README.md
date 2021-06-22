# yolo.py
<h3 align="center">A custom Python implementation of YOLOv5 algorithm</h2>
<p align="center">
  <img src="https://drive.google.com/uc?export=view&id=19mqTy_G3Ut54NSiB9ooZ_gKwRBsKjt0-"/>
  <br>
</p>

## Installation
The first step that we gotta do is downloading all depencencies necessary to run the 
[YOLOv5](https://github.com/ultralytics/yolov5) model. To do that, you need to have 
`pip` installed (Python3.6+ is required to use YOLO, so the pip version must follow it)

```shell
$ pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt
```

After that, all requirement are gonna be installed and we're ready to use the algorithm.

## Usage

### Simple example
```python
import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Image
img = 'https://ultralytics.com/images/zidane.jpg'

# Inference
results = model(img)

# Printing the results
results.print()
```

The above example takes a picture from the website and make the classification over that image. The
resulsts are, them stored at `results` and we can print them on terminal using `results.print()` 
function or show the image ith the objects detected with `results.show()`.

### Running
Given a set of images, the algorithm iterates inside the folder with those images and, for each picture, 
it makes a prediction to check whether there is a person (or an animal)/vehicle or not.<br>
To run, we just need to open the terminal at the project directory and type

```shell
$ python3 main.py pics_folder target_folder
```

It's important to say, again, that Python 3.6+ is needed to run because of the Yolov5 model.

## References

## Authors
