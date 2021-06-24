import torch
from PIL import Image, ImageDraw
from shapely.geometry import LineString
import utilities

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
    people = [row for index, row in df.iterrows() if row["name"] in utilities.PASSERBY_TARGET]
    vehicles = [row for index, row in df.iterrows() if row["name"] in utilities.VEHICLE_TARGET]

    return people, vehicles

def draw_lines(elements, draw, color_yes, color_no, square, area, outline):
    # The function below is responsible for painting/drawing the box arround the 
    # element (a passerby or a vehicle) or paint the current car boxes depending
    # on the intersection of the objects within the car's bounding boxes.
    # 
    # elements  -> refers to the objects that we had detected
    # draw      -> the drawing object, used to draw the lines/polygons
    # color_yes -> color that the lines/polygons are gonna receive in the case of
    #            a positive detection
    # color_no  -> color that lines/polygons are gonna receive if there were no
    #              detection
    # square    -> a vector of LineStrings with all sides of the safe area
    # area      -> the safe area that the current car has
    # outline   -> the color that the elements' box are gonna receive 
    if elements:
        has = False
        for element in elements:
            draw.rectangle([(element["xmin"], element["ymin"]), 
                            (element["xmax"], element["ymax"])], 
                            outline=outline)
            line = LineString([(element["xmin"], element["ymax"]), 
                                (element["xmin"], element["ymin"])])

            if not has:
                for square_line in square:
                    if line.intersects(square_line):
                        has = True

            if has:
                draw.line(area, fill=color_yes, width=5)
            else:
                draw.line(area, fill=color_no, width=5)
    else:
        draw.line(area, fill=color_no, width=5)

def start(path, target_folder):
    # Starts the detection process, using the path and target passed as args.
    init_model()
    img_count = 1
    files = utilities.get_img_files(path)

    for file in files:
        passersby, vehicles = detect(file)

        im = Image.open(file)
        draw = ImageDraw.Draw(im)

        if not passersby and not vehicles:        
            draw.line(utilities.PASSERBY_AREA, fill ="green", width=5)
            draw.line(utilities.VEHICLE_AREA, fill ="green", width=5)
        else:
            draw_lines(passersby, draw, "red", "green", utilities.PASSERBY_SQUARE, 
                    utilities.PASSERBY_AREA, "red")
            draw_lines(vehicles, draw, "yellow", "green", utilities.VEHICLE_SQUARE, 
                    utilities.VEHICLE_AREA, "cyan")

        im.convert('RGB').save('{}/{}.jpg'.format(target_folder, img_count))
        img_count += 1
        del im
        del draw