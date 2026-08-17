# 读入点位信息
with open('E:/treepaper/Mapping-ray-Wang/data/add/point_names_1.txt', 'r') as file:
    lines = file.readlines()
    lat = []
    lng = []
    i = 0
    for info in lines:
        parts = info.split("\t")
        if parts[0] != '\n':
            lng.append(float(parts[0])) # 预测点
            lat.append(float(parts[1]))

def partition(lat_all, lng_all, ind):
    lat = []
    lng = []
    i = 1
    while i < len(ind):
        lat.append(lat_all[ind[i]])
        lng.append(lng_all[ind[i]])
        i = i + 1
    max1, max2, min1, min2 = max(lat), max(lng), min(lat), min(lng)
    p1 = (max1 - min1)/2
    p2 = (max2 - min2)/2
    index = []
    for i in range(4):
        index.append([])
    index[0].append([min1, min1+p1, min2, min2+p2])
    index[1].append([min1, min1+p1, min2+p2, max2])
    index[2].append([min1+p1, max1, min2, min2+p2])
    index[3].append([min1+p1, max1, min2+p2, max2])
    k = 1
    while k < len(ind):
        i = ind[k]
        if (lat_all[i] <= (min1 + p1*1.1)) & (lng_all[i] <= (min2 + p2*1.1)):
            index[0].append(i)
        if (lat_all[i] <= (min1 + p1*1.1)) & (lng_all[i] >= (min2 + p2*0.9)):
            index[1].append(i)
        if (lat_all[i] >= (min1 + p1*0.9)) & (lng_all[i] <= (min2 + p2*1.1)):
            index[2].append(i)
        if (lat_all[i] >= (min1 + p1*0.9)) & (lng_all[i] >= (min2 + p2*0.9)):
            index[3].append(i)
        k = k + 1
    for i in range(4):
        if len(index[i]) > 5000:
            index_1 = partition(lat_all, lng_all, index[i])
            index[i] = index_1
    
    return index

def flatten_nested_list(nested_list):
    flattened_list = []
    for item in nested_list:
        if isinstance(item, list):
            flattened_list.extend(flatten_nested_list(item))
        else:
            flattened_list.append(item)
    return flattened_list


ind = []
max1, max2, min1, min2 = max(lat), max(lng), min(lat), min(lng)
ind.append([min1, max1, min2, max2])
for i in range(len(lat)):
    ind.append(i)
index = partition(lat, lng, ind)

# 读入点位信息
with open('E:/treepaper/Mapping-ray-Wang/data/add/point_names.txt', 'r') as file:
    lines_p = file.readlines()
    tree_coordinates_all = []
    confidence_all = []
    dis_all = []
    for info in lines_p:
        parts = info.split("\t")
        if parts[0] != '\n':
            name = parts[4].replace('\n', '')
            tree_coordinates_all.append([float(parts[1]), float(parts[0]), name]) # 预测点
            confidence_all.append(float(parts[3]))
            dis_all.append(float(parts[2]))

# 读入种类信息
#species_all = []
#with open('F:/treepaper/species_1.txt', 'r') as file:
#    lines = file.readlines()
#    for line in lines:
#        if line != '\n':
#            species_all.append(line.split('\t')[0])

result = []
index_flatten = flatten_nested_list(index)

i = 4
index_flatten_1 = []
start = 0
while i < len(index_flatten) - 1:
    if (type(index_flatten[i + 1]) == float) & (type(index_flatten[i]) == int):
        end = i
        index_flatten_1.append(index_flatten[start:end])
        start = i + 1
    i = i + 1
index_flatten_1.append(index_flatten[start:i])
with open('E:/treepaper/Mapping-ray-Wang/data/add/index.txt', 'w') as file:
    for item in index_flatten_1:
        file.write(str(item) + '\n')


  