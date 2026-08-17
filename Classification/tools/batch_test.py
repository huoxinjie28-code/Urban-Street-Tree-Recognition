from argparse import ArgumentParser
import os
import sys
sys.path.insert(0,os.getcwd())
import torch
import cv2
import csv
from utils.inference import inference_model, init_model
from core.visualization.image import imshow_infos
from utils.train_utils import get_info, file2dict
from models.build import BuildNet
from PIL import Image
import numpy as np
import json
import re
import copy
def main():
    parser = ArgumentParser()
    parser.add_argument('path', help='Path of batch images')
    parser.add_argument('config', help='Config file')
    parser.add_argument(
        '--classes-map', default='datas/annotations.txt', help='classes map of datasets')
    parser.add_argument(
        '--device', default='cpu', help='Device used for inference')
    parser.add_argument(
        '--save-path',
        help='The path to save prediction image, default not to save.')
    parser.add_argument('--show', action='store_true', help='Show image classification results')
    args = parser.parse_args()
    classes_names, label_names = get_info(args.classes_map)
    # build the model from a config file and a checkpoint file
    model_cfg, train_pipeline, val_pipeline, data_cfg, lr_config, optimizer_cfg = file2dict(args.config)
    if args.device is not None:
        device = torch.device(args.device)
    else:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    model = BuildNet(model_cfg)
    model = init_model(model, data_cfg, device=device, mode='eval')
    image_maps = dict()
    for file in os.listdir(args.path):
        image_maps[file] = cv2.imread(os.path.join(args.path,file))
    out_path = None
#    json_folder = "D:/Awesome-Backbones/yolov11-Zhuhai-category-cropped_json"
    for name in image_maps:
        if args.save_path:
            out_path = os.path.join(args.save_path,name)
        img = image_maps[name]
        # get single test results
        result = inference_model(model, img, val_pipeline, classes_names,label_names)
        # put the results to img
        img_show = imshow_infos(img, result,show = False,out_file=out_path)
        predicted_class = result['pred_class']
        #if predicted_class=='Banyan':
        #    label=0
        #elif predicted_class=='Chittagong-chickrassy':
        #    label=1
        #elif predicted_class=='Prunus-dulcis':
        #    label=2
        #elif predicted_class=='Palm':
        #    label=3
        #elif predicted_class=='Others':
        #    label=4
        confidence = result['pred_score']
        #json_filepath = os.path.join(json_folder, name + 'crop.json')
        #json_file_name = name.split("_crop")[0] + "_crop.json"
        #json_filepath = os.path.join(json_folder, json_file_name)
        #match = re.search(r'crop(\d+)', name)
        #if match:
        #    crop_num = int(match.group(1))
        #    with open(json_filepath, 'r') as f:
        #        data = json.load(f)
        #        shape=data["shapes"]
        #        shape[crop_num]["label"] = label
        #    with open(json_filepath, "w") as f:
        #        json.dump(data, f,indent=4)
        with open("D:/Awesome-Backbones/NewYork-classes-yolov11.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name,predicted_class, confidence])
        if args.show:
            cv2.namedWindow('video', 0)
            cv2.imshow('video',img_show)
        #q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
