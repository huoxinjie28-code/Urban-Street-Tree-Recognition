import pyproj
from openpyxl import Workbook
import numpy as np
from scipy.spatial import KDTree
from geographiclib.geodesic import Geodesic

# 经纬度转XY
def coordinates_to_XY(lat, lng):
    utm = pyproj.Proj(proj="utm", zone=18, ellps="WGS84")
    x, y = utm(lat, lng)

    return x, y

def coordinates_List_to_XY_List(coordinates):
    XY_List = []
    for coord in coordinates:
        lat, lng = coord
        xy = coordinates_to_XY(lat, lng)
        XY_List.append(xy)
    return XY_List

fiLe_path = 'Mapping//data//add//'
#打开文件以读取内容
with open(fiLe_path + 'result.txt', 'r') as file:
    lines = file.readlines()

    point_final = []
    for info in lines:
        parts = info.split("\t")
        if parts[0] != '\n':
            point_final.append([float(parts[1]), float(parts[0])])

with open(fiLe_path + 'new_york_r4_real.txt', 'r') as file:
    lines0 = file.readlines()
    clean_line = []
    # 跳过第一行
    point_list = []
    for i in range(1, len(lines0)):
        parts = lines0[i].split(",")
        k = len(parts)
        point_list.append([float(parts[k-2]), float(parts[k-1])])

point_final_0 = coordinates_List_to_XY_List(point_final)
point_list_0 = coordinates_List_to_XY_List(point_list)

# 将点列表转换为数组格式
point_set = np.array(point_list_0)

# 构建kd树
kdtree = KDTree(point_set)

# 将查询点列表转换为数组格式
query_point_set = np.array(point_final_0)

# 查询最近的点
dist, idx = kdtree.query(query_point_set)

# 打印最近的点和距离
for i in range(len(point_final)):
    print("查询点：", point_final[i])
    print("最近的点：", point_list[idx[i]])
    print("距离：", dist[i])
    print()

true = 0
false = 0
threshold_min = 5
for i in range(len(dist)):
    if float(dist[i]) < threshold_min:
        true = true + 1
    else:
        false = false + 1

Precision = true/len(query_point_set)
result = [x for x in dist if x < 60]
print(np.median(result), np.min(result), np.mean(result), np.std(result))

kdtree_0 = KDTree(query_point_set)
# 查询最近的点
dist, idx = kdtree_0.query(point_set)

true = 0
false = 0
for i in range(len(dist)):
    if float(dist[i]) < threshold_min:
        true = true + 1
    elif float(dist[i]) <10:
        false =false + 1
print(len(query_point_set))
print("Precision：", Precision)
Recall = true/(true+false)
print("Recall", Recall)


print(len(point_final))
print(true+false)

with open(fiLe_path + 'result_c.txt', 'w') as file:
    for item in point_final:
        file.write(str(item[0]) + '\t' + str(item[1]) + '\n')
