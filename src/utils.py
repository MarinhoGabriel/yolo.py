from shapely.geometry import LineString
import os
import glob

# The passerby area is the car area which is considered safe, when
# there is no one inside of it. In other words, the PASSERBY_AREA is
# an area used to make the decisions about driving, e.g., when a person
# intersects this area, a decicion needa be taken (brake or turn).
PASSERBY_AREA = [(640 - 365, 720), 
                    (640 - 115, 720 - 250), 
                    (640 + 115, 720 - 250), 
                    (640 + 365, 720)]

# The square is just another way to represent the PASSERBY_AREA. However,
# instead of a list of coorinates, we have a list of LineStrings, used to
# check the intersection between the passerby's box and the safe area.
PASSERBY_SQUARE = [LineString([(640 - 365, 720), (640 - 115, 720 - 250)]), 
                    LineString([(640 - 115, 720 - 250), (640 + 115, 720 - 250)]),
                    LineString([(640 + 115, 720 - 250), (640 + 365, 720)]), 
                    LineString([(640 - 365, 720), (640 + 365, 720)])]

# As the PASSERBY_AREA, the vehicle area works the same: it's an safe
# area, but, now, considering vehicles instead of people (or animals).
# It's a little bit lager than the passerby area, but works as well.
VEHICLE_AREA = [(640 - 485, 720), 
            (640 - 150, 720 - 250), 
            (640 + 150, 720 - 250), 
            (640 + 485, 720)]

# The square is just another way to represent the VEHICLE_AREA. However,
# instead of a list of coorinates, we have a list of LineStrings, used to
# check the intersection between the vehicle's box and the safe area.
VEHICLE_SQUARE = [LineString([(640 - 485, 720),(640 - 150, 720 - 250)]), 
            LineString([(640 - 150, 720 - 250), (640 + 150, 720 - 250)]),
            LineString([(640 + 150, 720 - 250), (640 + 485, 720)]), 
            LineString([(640 - 485, 720), (640 + 485, 720)])]

# The following array is responsible for storing all classes that are going
# to be considered as passersby. All of the following classes are going to
# define the color of the PASSERBY_AREA square.
PASSERBY_TARGET = ["person", "dog", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", 
                "zebra", "giraffe", "kite", "teddy bear"]

# The following array works as the aboce one: it's an array of vehicles 
# classes that are going to be avoided by the car.
VEHICLE_TARGET = ["car", "bus", "truck", "motorbike", "bicycle"]

def get_img_files(path):
    # The following function is responsible for getting all the pictures that we are going to
    # detect the objects. It has a parameter, which is the base directory of all of them.
    # path = "/mnt/Development/passerby_crossing_between_cars0/passerby_crossing_between_cars0/semantic_segmentation"
    return sorted(filter(os.path.isfile, glob.glob(path + '/*')))