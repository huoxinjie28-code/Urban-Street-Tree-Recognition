import os
import json
import numpy as np
from collections import defaultdict

# Function to calculate IoU
def calculate_iou(box1, box2):
    x1 = max(box1[0][0], box2[0][0])
    y1 = max(box1[0][1], box2[0][1])
    x2 = min(box1[1][0], box2[1][0])
    y2 = min(box1[1][1], box2[1][1])
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)

    box1_area = (box1[1][0] - box1[0][0]) * (box1[1][1] - box1[0][1])
    box2_area = (box2[1][0] - box2[0][0]) * (box2[1][1] - box2[0][1])
    union_area = box1_area + box2_area - inter_area
    if union_area == 0:
        return 0
    return inter_area / union_area

# Directory paths
ground_truth_dir = "E:/treepaper/zhuhai-map/gtjson"  # Replace with your ground truth folder path
detection_dir = "E:/treepaper/zhuhai-map/zhuhaicropjson-last"       # Replace with your detection folder path

# Parse files
ground_truth_files = [f for f in os.listdir(ground_truth_dir) if f.endswith('.json')]
detection_files = [f for f in os.listdir(detection_dir) if f.endswith('.json')]

# Results storage
class_ap = defaultdict(lambda: {'tp': 0, 'fp': 0, 'fn': 0})
iou_thresholds = np.linspace(0.5, 0.95, 10)

# Process each ground truth file
for gt_file in ground_truth_files:
    gt_path = os.path.join(ground_truth_dir, gt_file)
    det_path = os.path.join(detection_dir, gt_file.replace(".json", "crop.json"))
    
    if not os.path.exists(det_path):
        continue

    with open(gt_path, 'r') as gt_f, open(det_path, 'r') as det_f:
        gt_data = json.load(gt_f)
        det_data = json.load(det_f)

        gt_shapes = {shape['label']: shape['points'] for shape in gt_data.get('shapes', [])}
        det_shapes = {shape['label']: shape['points'] for shape in det_data.get('shapes', [])}
        matched = set()
        for label, gt_points in gt_shapes.items():
            if label not in det_shapes:
                class_ap[label]['fn'] += 1
                continue

            found = False
            iou = calculate_iou(gt_points, det_shapes[label])
            if iou > 0.5:
                class_ap[label]['tp'] += 1
                matched.add(tuple(map(tuple, det_shapes[label])))
                found = True
                break

            if not found:
                class_ap[label]['fn'] += 1

        # Count false positives
        for label, det_points_list in det_shapes.items():
            for det_points in det_points_list:
                if tuple(map(tuple, det_shapes[label])) not in matched:
                    class_ap[label]['fp'] += 1

# Calculate AP metrics
results = {}
for label, counts in class_ap.items():
    tp = counts['tp']
    fp = counts['fp']
    fn = counts['fn']
    precision = tp / (tp + fp) if tp + fp > 0 else 0
    recall = tp / (tp + fn) if tp + fn > 0 else 0
    ap50 = precision * recall  # Simplified for IoU > 0.5
    ap_range = []
    for iou_thres in iou_thresholds:
        ap_range.append(precision * recall)  # Simplified, refine with proper calculation
    results[label] = {
        "ap50": ap50,
        "ap(50:95)": np.mean(ap_range),
    }

# Summarize total metrics
total_ap50 = np.mean([r["ap50"] for r in results.values()])
total_ap_range = np.mean([r["ap(50:95)"] for r in results.values()])

# Display results
import pandas as pd

results_df = pd.DataFrame.from_dict(results, orient='index')
results_df.loc["Total"] = {"ap50": total_ap50, "ap(50:95)": total_ap_range}

print(results_df)
