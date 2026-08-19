
from ultralytics import YOLO

model = YOLO("D:/ultralytics-main/yolo11n.pt")  
results = model.train(data="D:/ultralytics-main/tree.yaml", epochs=20, imgsz=640)
