from ultralytics import YOLO
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
# Load a model 这里选择预训练模型或者网络结构 有不同模型可以选择 我这使用yolov8n.pt
model = YOLO("D:/ultralytics-main/yolov8n.pt")  # load a pretrained model (recommended for training)
# Use the model0 data指定你的yaml文件，然后设置超参数
model.train(data="D:/ultralytics-main/tree-category.yaml", epochs=20,batch=16)  # train the model
