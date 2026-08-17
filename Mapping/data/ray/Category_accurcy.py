import pyproj
from openpyxl import Workbook
import numpy as np
from scipy.spatial import KDTree

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

# 创建一个字典，用于存储每个类别对应的树种
tree_categories_seoul = {
    "Platanus": ["悬铃木"],
    "Zelkova-Serrate": ["榉树", "李属"],
    "Ginkgo-biloba": ["银杏树"],
    "Others": ["枣树", "银枫", "Others"]
}

tree_categories_zhuhai = {
    "Others": ["Others"],
    "Palm":["Prunus dulcis"],
    "Banyan":["Banyan"],
    "Chittagong-chickrassy":["Chittagong chickrassy"],
    "Prunus-dulcis":["Palm"]
}

tree_categories = tree_categories_zhuhai
species = []

fiLe_path = 'G://6.13//add//'
#打开文件以读取内容
with open(fiLe_path + 'real.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        if line != '\n':
            parts = line.split('\t')
            species.append([parts[0], float(parts[1]), float(parts[2].replace('"', '').replace('\n', ''))])

real = []
real_s = []
k = []
#打开文件以读取内容
with open(fiLe_path + 'real.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        parts = line.split(',')
        lat = float(parts[2])
        lng = float(parts[1])
        index = [index for index, value in enumerate(species) if (abs(value[1]- lat) < 0.0001) & (abs(value[2] - lng) < 0.0001)]
        if len(index) > 0:
            for category, trees in tree_categories.items():
                specie = species[index[0]][0]
                if specie in trees:
                    s = category
                    break
            real.append([lng, lat])
            real_s.append(s)
            k.append([lng, lat, species[index[0]][0]])

# real = []
# real_s = []
# with open('G://6.13//add//zhuhai_real.txt', 'r') as file:
#     lines = file.readlines()
#     for line in lines:
#         parts = line.split(',')
#         real.append([float(parts[1]), float(parts[2])])
#         if len(parts) > 3:
#             specie = parts[3].replace('\n','')
#         else:
#             specie = 'Chittagong chickrassy'
#         for category, trees in tree_categories.items():
#             if specie in trees:
#                 s = category
#                 break
#         real_s.append(s)
#
# result = []
# result_s = []
# #打开文件以读取内容
# with open('G://lunwen//final//zhuhai_result.txt', 'r') as file:
#     lines = file.readlines()
#     for line in lines:
#         if line != '\n':
#             parts = line.split(',')
#             result.append([float(parts[2]), float(parts[1])])
#             result_s.append(parts[4].replace('\n', ''))

result = []
result_s = []
#打开文件以读取内容
with open(fiLe_path + 'result.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        if line != '\n':
            parts = line.split('\t')
            result.append([float(parts[0]), float(parts[1])])
            result_s.append(parts[2].replace('\n', ''))

result_XY = coordinates_List_to_XY_List(result)
real_XY = coordinates_List_to_XY_List(real)

result_set = np.array(result_XY)
real_set = np.array(real_XY)

# recall
kdtree = KDTree(result_set)
dist, idx = kdtree.query(real_set)

true = 0
true_s = 0
threshold_min = 6    # 阈值
for i in range(len(real_set)):
    if dist[i] < threshold_min:
        true = true + 1
        if real_s[i] == result_s[idx[i]]:
            true_s = true_s + 1

c_recall = true/len(real_set)
s_recall = true_s/len(real_set)
key_tree_recall = []
value_tree_recall = []
for key, value0 in tree_categories.items():
    true = 0
    index = []
    for index_tree, value in enumerate(real_s):
        if value == key:
            index.append(index_tree)
    if len(index) > 0:
        for i in index:
            if (result_s[idx[i]] == key) & (dist[i] < threshold_min):
                true = true + 1
        key_tree_recall.append(key)
        value_tree_recall.append(true/len(index))
    else:
        key_tree_recall.append(key)
        value_tree_recall.append(0)

# precision
kdtree = KDTree(real_set)
dist, idx = kdtree.query(result_set)

true = 0
true_s = 0
for i in range(len(result_set)):
    if dist[i] < threshold_min:
        true = true + 1
        if real_s[idx[i]] == result_s[i]:
            true_s = true_s + 1

c_precision = true/len(result_set)
s_precision = true_s/len(result_set)

key_tree_precision = []
value_tree_precision = []
for key, value0 in tree_categories.items():
    true = 0
    index = [index for index, value in enumerate(result_s) if value == key]
    print(len(index))
    if len(index) > 0:
        for i in index:
            if (real_s[idx[i]] == key) & (dist[i] < threshold_min):
                true = true + 1
        key_tree_precision.append(key)
        value_tree_precision.append(true/len(index))
    else:
        key_tree_precision.append(key)
        value_tree_precision.append(0)

F1_c = (2*c_precision*c_recall)/(c_precision+c_recall)
F1_s = (2*s_precision*s_recall)/(s_precision+s_recall)

d_r = []
for d in dist:
    if d < 20:
        d_r.append(d)

print(len(result_XY), len(real_XY))
print(np.median(np.sort(d_r)), np.min(d_r), np.mean(d_r))
print(c_recall, c_precision, s_recall, s_precision)
print(F1_c, F1_s)
for i in range(4):
    print('tree_name: ', key_tree_precision[i], 'recall: ', value_tree_recall[i], 'precision: ', value_tree_precision[i])

