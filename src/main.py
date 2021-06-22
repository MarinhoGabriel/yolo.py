import sys

from yolo import start

path = str(sys.argv[1])
print("Starting the detection over " + path)
start(path)