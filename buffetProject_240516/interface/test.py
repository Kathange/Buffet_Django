# name_classes  =  ['corn','duck_blood','sweet_potato','mung_bean_noodles','loofah','chicken','chicken_thigh','fried_drumstick','fried_mochi_waste','bone']

# # 拿取詳細資訊，show:單一品項詳細資訊 ; total:總詳細資訊
# read_merged_list = []
# with open('./static/file/merged_data.txt', 'r') as file:
#     read_merged_list = [list(map(float, line.strip().split(','))) for line in file]
# show = []
# total = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# print(len(read_merged_list)-1)
# for i in range(len(name_classes)-1):
#     print("i: ",i)
#     if read_merged_list[i][0] == 0:
#         continue
#     show.append([name_classes[i]] + read_merged_list[i])
#     print("read_merged_list: ", read_merged_list[i])
#     for j in range(len(read_merged_list[i])):
#         total[j] += read_merged_list[i][j]
#         total[j] = round(total[j], 3)
# data = show.copy()
# data.append(['Total'] + total)

# print(data)



name_classes  =  ['corn','duck_blood','sweet_potato','mung_bean_noodles','loofah','chicken','chicken_thigh','fried_drumstick','fried_mochi_waste','bone']
volume = [1,2,3,4,5,6,7,8,9,10,11,12,13]
if 'bone' in name_classes:
    # 获取字符串的位置
    boneIndex = name_classes.index('corn')
bonedepth = volume[boneIndex]
print(bonedepth)

# 初始化一个字典来存储每个元素的位置
positions = {}
food_names_list = ['fried_drumstick', 'chicken', 'chicken_thigh']
# 遍历 food_names_list 列表
for food in food_names_list:
    if food in name_classes:
        # 获取每个元素的位置
        position = name_classes.index(food)
        # 获取该位置对应的 volume 值
        current_volume = volume[position]
        # print(f"{food} 在 position {position} 对应的 volume 值是: {current_volume}")
        # 这里可以修改该位置的 volume 值
        volume[position] = current_volume * 2  # 示例：将当前 volume 值翻倍

# 打印修改后的 volume 列表
print("修改后的 volume 列表:", volume)

