import csv

# 指定CSV和TXT文件的路径
csv_file_path = 'NewYorkR4.csv'
txt_file_path = 'Mapping/data/NewYorkR4c.txt'

# 打开CSV文件并读取内容
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # 跳过表头
    next(csv_reader)
    
    # 打开TXT文件准备写入
    with open(txt_file_path, mode='w', encoding='utf-8') as txt_file:
        for row in csv_reader:
            # 将每一行转换为字符串并写入TXT文件
            txt_file.write(','.join(row) + '\n')

print("数据已成功写入到TXT文件中！")
