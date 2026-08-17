#coding=utf-8
import os
import arcpy
from math import tan, radians
from openpyxl import Workbook # type: ignore
import shutil
import re

# 读取字符串中的整数
def extract_int(string):
    lists=[]
    for i in string:
        j=i
        try:
            if type(int(j))==int:
                lists.append(i)
        except:
            continue

    return int(''.join(lists))

# 创建新的要素类
def create_ray_feature_class(file_path):
    # 创建一个新的要素类来存储射线
    spatial_reference = arcpy.SpatialReference(4326)  # 这里使用WGS84坐标系
    arcpy.CreateFeatureclass_management(os.path.dirname(file_path), os.path.basename(file_path), "POLYLINE", spatial_reference=spatial_reference)

# 清空文件夹
def empty_folder(file_path):
    parent_folder = os.path.dirname(file_path)
    if os.path.exists(parent_folder):
        for item in os.listdir(parent_folder):
            item_path = os.path.join(parent_folder, item)
            if os.path.isdir(item_path):
                # 如果是子文件夹，递归清空子文件夹
                shutil.rmtree(item_path)
            else:
                # 如果是文件，直接删除
                os.remove(item_path)
        print("文件夹已清空，但文件夹本身保留。")
    else:
        print("文件夹不存在。无需清空。")

# 创建射线集
def add_ray_to_feature_class(output_path, ray_point, ray_direction):
    # 使用 InsertCursor 向要素类中添加射线
    cursor = arcpy.da.InsertCursor(output_path, ["SHAPE@"])
    if ray_direction <= 180:
        ray_line = arcpy.Polyline(arcpy.Array([ray_point, arcpy.Point(ray_point.X + 1, ray_point.Y + 1 * 1/tan(radians(ray_direction)))]), arcpy.SpatialReference(4326))
    if 180 < ray_direction:
        ray_line = arcpy.Polyline(arcpy.Array([ray_point, arcpy.Point(ray_point.X - 1, ray_point.Y - 1 * 1/tan(radians(ray_direction)))]), arcpy.SpatialReference(4326))
    cursor.insertRow([ray_line])
    del cursor


height = 512
width = 512
fiLe_path = 'E:/treepaper/Mapping-ray-Wang/data/addNewYork-Yolov11/'

output_feature_class = fiLe_path + "ray//ray.shp"
empty_folder(output_feature_class)
create_ray_feature_class(output_feature_class)

names = []
coordinate = []
confidence = []
with open(fiLe_path + 'NewYorkR4results.txt', 'r') as f:
#    lines = f.readlines()
#    for line in lines:
#        parts = line.split('\t')
#        x_mid = parts[1].split('.')[0]
#        names.append([parts[0].replace('"', ' ').replace('.jpg', ' ').strip(), x_mid])
    for line in f:
        parts = line.split(',')
        imagename=line.split(' ')
      # 提取纬度和经度
        lat= float(parts[0])
        lng = float(parts[1].split('_')[0])
        match = re.search(r"_d(\d+)_", parts[1])
        if match:
            north= match.group(1)
        x_mid=int(float(parts[1].split(' ')[1]))
        con = float(parts[1].split(' ')[2])
        #info = parts[0].replace('"', ' ').replace('.jpg', ' ').strip().split('_')
        #k = len(info)
        #lat, lng, north = info[0].split(',')[0], info[0].split(',')[1], extract_int(info[k-3])
        #con = parts[2]
        start_index = parts[1].find('z2_') + len('z2_')
        # 提取 'z2_' 后面的数字，直到遇到空格
        number_str = parts[1][start_index:].split(' ')[0] 
        direction = (float(x_mid)/width)*90 + float(number_str) - north
        if direction < 0:
            direction = direction + 360
        add_ray_to_feature_class(output_feature_class, arcpy.Point(lng, lat), direction)
        coordinate.append([lng, lat])
        confidence.append(con)
        names.append(f"{imagename[0]}"+f"{{{x_mid}}}.jpg")

n = []
for name in names:
    n.append(name[0] + '{' + name[1] + '}.jpg')

with open(fiLe_path + 'coordinate.txt', 'w') as file:
    for item in coordinate:
        file.write(str(item[0]) + '\t' + str(item[1]) + '\n')

with open(fiLe_path + 'confidence.txt', 'w') as file:
    for item in confidence:
        file.write(str(item)+'\n')

with open(fiLe_path + 'names.txt', 'w') as file:
    for item in names:
        file.write(str(item) + '\n')


