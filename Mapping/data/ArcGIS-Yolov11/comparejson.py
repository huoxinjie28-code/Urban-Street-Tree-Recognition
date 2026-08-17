import json
from collections import defaultdict
import numpy as np
import os
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
def get_boxes_from_json(json_data):
    boxes = defaultdict(list)
    for shape in json_data['shapes']:
        label = shape['label']
        points = shape['points']
        boxes[label].append(points)
    return boxes
def calculate_iou(box1, box2):
    x1, y1, w1, h1 = box1[0][0],box1[0][1],box1[1][0]-box1[0][0],box1[1][1]-box1[0][1]
    x2, y2, w2, h2 = box2[0][0],box2[0][1],box2[1][0]-box2[0][0],box2[1][1]-box2[0][1]
    inter_x = max(x1, x2)
    inter_y = max(y1, y2)
    inter_w = max(0, min(x1 + w1, x2 + w2) - inter_x)
    inter_h = max(0, min(y1 + h1, y2 + h2) - inter_y)

    inter_area = inter_w * inter_h
    box1_area = w1 * h1
    box2_area = w2 * h2
    iou = inter_area / (box1_area + box2_area - inter_area)
    return iou
def calculate_precision_recall(gt_boxes, pred_boxes, iou_threshold):
    # Calculate precision and recall for object detection
    tp = np.zeros(5)
    fp = np.zeros(5)
    fn = np.zeros(5)

    # Loop through each class label
    for label in gt_boxes.keys():
        gt_label_boxes = gt_boxes[label]
        pred_label_boxes = pred_boxes[label]
        
        for pred_box in pred_label_boxes:
            iou_max = -np.inf
            for gt_box in gt_label_boxes:
                iou = calculate_iou(pred_box, gt_box)
                if iou > iou_max:
                    iou_max = iou
            if iou_max >= iou_threshold:
                tp[label] += 1
            else:
                fp[label] += 1
                
        fn[label] = len(gt_label_boxes) - tp[label]

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    return precision, recall
def compute_detection_metrics(gt_boxes, pred_boxes, iou_threshold):
    precision, recall = calculate_precision_recall(gt_boxes, pred_boxes, iou_threshold)
    ap_results = []
    ap50_results = []
    ap75_results = []
    for label in range(5):
        ap = 0
        ap50 = 0
        ap75 = 0
        for t in np.arange(0, 1.1, 0.1):
            mask = recall[label] >= t
            if np.any(mask):
                p_max = np.max(precision[label][mask])
                ap += p_max / 11
                if t >= 0.5:
                    ap50 += p_max / 11
                if t >= 0.75:
                    ap75 += p_max / 11
        ap_results.append(ap)
        ap50_results.append(ap50)
        ap75_results.append(ap75)

    mAP = np.mean(ap_results)
    mAP50 = np.mean(ap50_results)
    mAP75 = np.mean(ap75_results)

    return ap_results, ap50_results, ap75_results, mAP, mAP50, mAP75

def main(gt_json_dir, pred_json_dir):
    all_ap_results=[]
    all_ap50_results=[]
    for gt_file in os.listdir(gt_json_dir):
        gt_json_file = os.path.join(gt_json_dir, gt_file)
        pred_json_file = os.path.join(pred_json_dir, gt_file.replace('.json', '_crop.json'))
        gt_shapes = load_json_file(gt_json_file)
        pred_shapes = load_json_file(pred_json_file)
        gt_boxes = get_boxes_from_json(gt_shapes)
        pred_boxes = get_boxes_from_json(pred_shapes)
        iou_threshold = 0.5
        ap_results, ap50_results, ap75_results, mAP, mAP50, mAP75 = compute_detection_metrics(gt_boxes, pred_boxes, iou_threshold)
       
        all_ap_results.append(ap_results)
        all_ap50_results.append(ap50_results)
        #print("AP75 Results:", ap75_results)
        #print("mAP:", mAP)
        #print("mAP50:", mAP50)
        #print("mAP75:", mAP75)
    print("All AP results:", all_ap_results)
    print("All AP50 results:", all_ap50_results)
if __name__ == "__main__":
    gt_json_dir = "E:/treepaper/comparezhuhai-json-category/yolov11-Zhuhai-category-json-4classes"
    pred_json_dir = "E:/treepaper/comparezhuhai-json-category/yolov11-Zhuhai-category-cropped_json"
    main(gt_json_dir, pred_json_dir)