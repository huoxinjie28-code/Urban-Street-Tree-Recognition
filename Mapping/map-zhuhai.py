import os
import json
import numpy as np
from collections import defaultdict
from scipy.optimize import linear_sum_assignment
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        shapes = data.get("shapes", [])
    return shapes
def calculate_iou(box1, box2):
    # 计算两个框的交并比
    x1, y1, w1, h1 = box1[0][0], box1[0][1], box1[1][0]-box1[0][0], box1[1][1]-box1[0][1]
    x2, y2, w2, h2 = box2[0][0], box2[0][1], box2[1][0]-box2[0][0], box2[1][1]-box2[0][1]
    inter_x = max(x1, x2)
    inter_y = max(y1, y2)
    inter_w = max(0, min(x1 + w1, x2 + w2) - inter_x)
    inter_h = max(0, min(y1 + h1, y2 + h2) - inter_y)
    inter_area = inter_w * inter_h
    box1_area = w1 * h1
    box2_area = w2 * h2
    iou = inter_area / (box1_area + box2_area - inter_area)
    return iou
def calculate_precision_recall(gt_boxes, pred_boxes, iou_threshold=0.5):
    if not gt_boxes or not pred_boxes:
        return 0, 0  # 处理空列表的情况
    num_gt = len(gt_boxes)
    num_pred = len(pred_boxes)

    # 计算所有预测框和真实框之间的 IoU 矩阵
    iou_matrix = np.zeros((num_gt, num_pred))
    for i in range(num_gt):
        for j in range(num_pred):
            iou_matrix[i, j] = calculate_iou(gt_boxes[i], pred_boxes[j])

    # 使用匈牙利算法找到最佳匹配
    row_ind, col_ind = linear_sum_assignment(-iou_matrix) #负号是因为linear_sum_assignment最小化成本

    tp = 0
    fp = 0
    fn = num_gt

    for i, j in zip(row_ind, col_ind):
        if iou_matrix[i, j] >= iou_threshold:
            tp += 1
            fn -= 1

    fp = num_pred - tp
    precision = tp / (tp + fp + 1e-6)
    recall = tp / (tp + fn + 1e-6)
    return precision, recall
def main(gt_json_dir, pred_json_dir):
    overall_results = defaultdict(list)
    mAPs = []

    for gt_file in os.listdir(gt_json_dir):
        gt_json_file = os.path.join(gt_json_dir, gt_file)
        pred_json_file = os.path.join(pred_json_dir, gt_file.replace('.json', '_crop.json'))
        gt_shapes = read_json(gt_json_file)
        pred_shapes = read_json(pred_json_file)

        labels = set([shape["label"] for shape in gt_shapes + pred_shapes])

        for label in labels:
            gt_boxes = [list(shape["points"]) for shape in gt_shapes if shape["label"] == label]
            pred_boxes = [list(shape["points"]) for shape in pred_shapes if shape["label"] == label]
            precision, recall = calculate_precision_recall(gt_boxes, pred_boxes)

            overall_results[label].append({
                    "Precision": precision,
                    "Recall": recall
                })
    for label, results in overall_results.items():
        precisions = [res["Precision"] for res in results]
        recalls = [res["Recall"] for res in results]
        AP =np.trapezoid(precisions, recalls)
        p = [p for p, r in zip(precisions, recalls) if r >= 0.5]
        r = [r for p, r in zip(precisions, recalls) if r >= 0.5]
        AP50 = np.trapezoid(p, r)
        p = [p for p, r in zip(precisions, recalls) if r >= 0.75]
        r = [r for p, r in zip(precisions, recalls) if r >= 0.75]
        AP75 = np.trapezoid(p, r)
        mAPs.append(AP)
        print(f"Class {label}:")
        print(f"AP: {AP}")
        print(f"AP50: {AP50}")
        print(f"AP75: {AP75}")
    mAP = np.mean(mAPs)
    print(f"mAP: {mAP}")
if __name__ == "__main__":
    gt_json_dir = "E:/treepaper/scomparezhuhai-json-category/yolov11-Zhuhai-category-json-4classe"
    pred_json_dir = "E:/treepaper/comparezhuhai-json-category/yolov11-Zhuhai-category-cropped_json"
    main(gt_json_dir, pred_json_dir)