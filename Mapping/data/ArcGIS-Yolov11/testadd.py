import re
names = []
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
with open('E:/treepaper/Mapping-ray-Wang/data/addNewYork-Yolov11/NewYorkR4results.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(',')
        imagename=line.split(' ') 
        x_mid = int(float(imagename[1]))
        names.append(f"{imagename[0]}"+f"{{{x_mid}}}.jpg")
print(names)
        #names.append([imagename[0].replace('"', ' ').replace('.jpg', ' ').strip(), x_mid])
        #print(names)
        #latitude = float(parts[0])
        #longitude = float(parts[1].split('_')[0])
      #match = re.search(r"_d(\d+)_", parts[1])
      #if match:
      #    true_north_angle= match.group(1)
      #start_index = parts[1].find('z2_') + len('z2_')

# 提取 'z2_' 后面的数字，直到遇到空格
      #number_str = parts[1][start_index:].split(' ')[0] 

# 将字符串转换为数字
      #number = int(number_str)
      #print(number)
      #xmid=float(parts[1].split(' ')[1])
      #confidence = float(parts[1].split(' ')[2])
      #data.append((latitude, longitude, true_north_angle, xmid, confidence))
  #return data
# 读取您的数据文件
#filename = "E:/treepaper/Mapping-ray-Wang/data/add/NewYorkR4c.txt"  # 请将 "your_data_file.txt" 替换为您的数据文件路径
#extracted_data = extract_data(filename)