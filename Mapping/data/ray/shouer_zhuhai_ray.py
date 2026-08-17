import pyproj
from openpyxl import Workbook
from geographiclib.geodesic import Geodesic

fiLe_path = 'G://6.13//add//'
all_info = []
# 打开文件以读取内容
with open(fiLe_path + 'intersect.txt', 'r') as file:
    lines = file.readlines()
    for info in lines:
        i = []
        parts = info.split(",")
        i.append([float(parts[5]), float(parts[6])])  # 预测点
        i.append([float(parts[7]), float(parts[8])])  # 拍摄点
        i.append(int(parts[3]))  # 射线ID
        print(i)
        all_info.append(i)

names = []
confidence = []
species = []
with open(fiLe_path + 'names.txt') as file:
    lines = file.readlines()
    for line in lines:
        names.append(line)

with open(fiLe_path + 'species.txt') as file:
    lines = file.readlines()
    for line in lines:
        species.append(line)

with open(fiLe_path + 'confidence.txt') as file:
    lines = file.readlines()
    for line in lines:
        confidence.append(line)

# 取距离每条射线的端点最近的点
# 寻找ID最大的射线
index = 0
max = 0
while index < len(all_info):
    if all_info[index][2] > max:
        max = all_info[index][2]
    index = index + 1

threshold = 40
index = 0
points = []
s = []
while index < max + 1:
    min = threshold
    k = 0
    index_id = [index_id for index_id, value in enumerate(all_info) if value[2] == index]
    print(index_id)
    for i in index_id:
        info = all_info[i]
        geodict = Geodesic.WGS84.Inverse(info[0][1], info[0][0], info[1][1], info[1][0])
        distance = geodict['s12']
        if distance < min:
            k = i
            min = distance
    if min != threshold:
        point = []
        id = all_info[k][2]
        point.append([all_info[k][0], min, confidence[id], names[id]])
        points.append(point)
        print(k)
        s.append(species[all_info[k][2]])

    index = index + 1

with open(fiLe_path + 'point_names.txt', 'w') as file:
    for item in points:
        file.write(str(item[0][0][0]) + '\t' + str(item[0][0][1]) + '\t' + str(item[0][1]) + '\t' + str(item[0][2]).replace('\n', '') + '\t' + str(item[0][3]))

with open(fiLe_path + 'sp.txt', 'w') as file:
    for item in s:
        file.write(str(item))
