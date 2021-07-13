import sys
import utilities
from yolo import start

path = None
target = None

if len(sys.argv) > 3:
    print("Converting video " + str(sys.argv[1]) + " to " + sys.argv[2])
    utilities.convert_video(sys.argv[1], sys.argv[2])
    path = sys.argv[2]
    target = sys.argv[3]
else:
    path = str(sys.argv[1])
    target = str(sys.argv[2])


print("Starting the detection over " + path)
start(path, target)