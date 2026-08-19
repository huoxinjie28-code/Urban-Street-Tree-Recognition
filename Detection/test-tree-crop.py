from ultralytics import YOLO
import os
import cv2
import json
model = YOLO("D:/ultralytics-main/runs/detect/train12/weights/best.pt")
input_folder = "D:/streeview_four_r3"
output_folder = "D:/03_11_whx/csv_r3"

cropped_folder = "D:/03_11_whx/image_r3"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
results_file = os.path.join(output_folder, "r3_results.txt")
with open(results_file, "w") as f:
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(input_folder, filename)

            results = model(image_path)
            for result in results:
                result.save(os.path.join(output_folder, filename)) 
            for result in results:
               boxes = result.boxes.xyxy
               confidences = result.boxes.conf
               cropped_images = []
               new_shapes = []
               for i, (box, confidence) in enumerate(zip(boxes, confidences)):
                   x_center = (box[0] + box[2]) / 2
                   img = cv2.imread(image_path)
                   f.write(f"{filename[:-4]} {x_center} {confidence.item():.4f}\n") 

                   x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                   cropped_img = img[y1:y2, x1:x2]
                   cropped_images.append(cropped_img)
                   cv2.imwrite(os.path.join(cropped_folder, filename[:-4] + f"_crop{i}"+f"{{{x_center}}}.jpg"), cropped_img)
                   new_shape = {
                   "label": 1,
                   "points": [[x1, y1], [x2, y2]],
                   "group_id": "null",
                   "description": "",
                   "shape_type": "rectangle",
                   "flags": {}
                   }
                   new_shapes.append(new_shape)

            data = {
               "version": "4.5.6",
               "flags": {},
               "shapes": new_shapes,
               "imagePath": filename
            }

        else:
           print("No detections found for:", filename)

print("Processing completed.")
