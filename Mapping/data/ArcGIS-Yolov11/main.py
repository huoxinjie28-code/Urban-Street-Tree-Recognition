
real_chinese = []
with open('G://lunwen//ray_right//seoul//seoul_real.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        if line != '"':
            print(line)

c = []
with open('G://6.13//add//real//1.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(',')
        c.append([parts[3], parts[4]])

