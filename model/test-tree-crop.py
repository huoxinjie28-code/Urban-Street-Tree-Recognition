from ultralytics import YOLO
import os
import cv2
import json
# 加载模型
model = YOLO("D:/ultralytics-main/runs/detect/train12/weights/best.pt")
# 输入图片文件夹路径
input_folder = "D:/streeview_four_r3"
# 输出检测结果文件夹路径
output_folder = "D:/03_11_whx/csv_r3"
# 裁剪图片文件夹路径
cropped_folder = "D:/03_11_whx/image_r3"

#json_out_folder = "D:/ultralytics-main/yolov11-Zhuhai-category-cropped_json"
# 创建输出文件夹和裁剪图片文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
#if not os.path.exists(cropped_folder):
#    os.makedirs(cropped_folder)
#if not os.path.exists(json_out_folder):
#    os.makedirs(json_out_folder, exist_ok=True)
# 创建用于保存所有检测结果的 txt 文件
results_file = os.path.join(output_folder, "r3_results.txt")
with open(results_file, "w") as f:
    # 遍历图片文件夹
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            # 获取图片路径
            image_path = os.path.join(input_folder, filename)

            # 检测图片
            results = model(image_path)

            # 保存带有目标检测框的图片
            for result in results:
                result.save(os.path.join(output_folder, filename))  # 使用原图片名保存
            # 提取检测结果
            for result in results:
               boxes = result.boxes.xyxy
               confidences = result.boxes.conf
               cropped_images = []
               new_shapes = []
               # 遍历每个检测框
               for i, (box, confidence) in enumerate(zip(boxes, confidences)):
                    # 获取检测框的中心坐标
                   x_center = (box[0] + box[2]) / 2
                   img = cv2.imread(image_path)
                    # 将中心坐标写入results.txt文件
                   f.write(f"{filename[:-4]} {x_center} {confidence.item():.4f}\n") 

                   # 裁剪图片
                   x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                   cropped_img = img[y1:y2, x1:x2]
                   cropped_images.append(cropped_img)
                   # 保存裁剪后的图片
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

            # 创建 JSON 数据
            data = {
               "version": "4.5.6",
               "flags": {},
               "shapes": new_shapes,
               "imagePath": filename
            }

            # 将 JSON 数据保存到文件
            # output_json = os.path.join(json_out_folder, filename[:-4]+"_crop.json")
            # with open(output_json, 'w') as file:
            #    json.dump(data, file, indent=4)

        else:
           print("No detections found for:", filename)

print("Processing completed.")