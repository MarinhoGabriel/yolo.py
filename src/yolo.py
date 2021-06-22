import torch
from PIL import Image, ImageDraw
from shapely.geometry import LineString
import utils

# Model used in the object detection step, using the YOLOv5 algorithm.
model = None

def init_model():
    # Initializes the model by loading the YOLOv5 model.
    global model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def detect(input_file):
    # The following function is responsible for making the detection and separating
    # into two arrays: one with all the passersby and another with all the vehicles
    # in the image. Those arrays are going to be used to know about the action
    # that the vehicle needa do.
    results = model(input_file)
    df = results.pandas().xyxy[0]
    people = [row for index, row in df.iterrows() if row["name"] in utils.PASSERBY_TARGET]
    vehicles = [row for index, row in df.iterrows() if row["name"] in utils.VEHICLE_TARGET]

    return people, vehicles

def draw_lines(elements, draw, color_yes, color_no, square, area):
    # The function below is responsible for painting/drawing the box arround the 
    # element (a passerby or a vehicle) or paint the current car boxes depending
    # on the intersection of the objects within the car's bounding boxes.
    if elements:
        has = False
        for element in elements:
            draw.rectangle([(element["xmin"], element["ymin"]), 
                            (element["xmax"], element["ymax"])], 
                            outline="red")
            line = LineString([(element["xmin"], element["ymax"]), 
                                (element["xmin"], element["ymin"])])

            if not has:
                for line in square:
                    if line.intersects(line):
                        has = True

            if has:
                draw.line(area, fill=color_yes, width=5)
            else:
                draw.line(area, fill=color_no, width=5)
    else:
        draw.line(area, fill=color_yes, width=5)

def start(path):
    # Starts the detection process, using the path passed as args.
    img_count = 1
    files = utils.get_img_files(path)

    for file in files:
        passersby, vehicles = detect(file)

        im = Image.open(file)
        draw = ImageDraw.Draw(im)

        if not passersby and not vehicles:        
            draw.line(utils.PASSERBY_AREA, fill ="green", width=5)
            draw.line(utils.VEHICLE_AREA, fill ="green", width=5)
        else:
            draw_lines(passersby, draw, "red", "green", utils.PASSERBY_SQUARE, utils.PASSERBY_AREA)
            draw_lines(passersby, draw, "red", "green", utils.VEHICLE_SQUARE, utils.VEHICLE_AREA)

        im.convert('RGB').save('results-semantic/{}.jpg'.format(img_count))
        img_count += 1
        del im
        del draw