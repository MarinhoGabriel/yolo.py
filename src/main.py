import sys

from yolo import start

path = str(sys.argv[1])
target = str(sys.argv[2])
print("Starting the detection over " + path)
start(path, target)