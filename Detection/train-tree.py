
from ultralytics import YOLO

model = YOLO("yolo11n.pt")  
results = model.train(data="tree.yaml", epochs=20, imgsz=640)
