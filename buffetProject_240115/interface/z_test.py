import matplotlib.pyplot as plt
import matplotlib
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from datetime import datetime
from PIL import Image, ImageDraw

# # 创建一个包含两个子图的图形
# fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

# # 创建第一个饼图并将其添加到第一个子图中
# labels1 = ['A', 'B', 'C']
# values1 = [30, 50, 20]
# ax1.pie(values1, labels=labels1)
# ax1.set_title('Pie chart 1')

# # 创建第二个饼图并将其添加到第二个子图中
# labels2 = ['D', 'E', 'F']
# values2 = [10, 60, 30]
# ax2.pie(values2, labels=labels2)
# ax2.set_title('Pie chart 2')

# # 添加图例和标题
# ax1.legend()
# ax2.legend()
# fig.suptitle('Merged pie charts')

# plt.savefig('test.png')









def crop_to_square_and_circle(input_path, output_path):
    # 打開圖片
    original_image = Image.open(input_path)
    # 確定圖片的寬度和高度
    width, height = original_image.size
    # 計算切割後的正方形大小
    size = min(width, height)
    # 計算切割的左上角位置，使正方形位於原始圖片的中心
    left = (width - size) // 2
    top = (height - size) // 2
    # 切割圖片
    cropped_square_image = original_image.crop((left, top, left + size, top + size))
    # 設置圓形半徑為正方形寬度的一半
    radius = size // 2
    # 創建一個具有 alpha 通道的全透明圖片
    circle_mask = Image.new("L", (size, size), 0)
    # 在圓形遮罩上畫一個白色的圓
    draw = ImageDraw.Draw(circle_mask)
    draw.ellipse((0, 0, size, size), fill=255)
    # 將遮罩應用於正方形圖片
    circular_image = Image.new("RGBA", (size, size))
    circular_image.paste(cropped_square_image, (0, 0))
    circular_image.putalpha(circle_mask)
    # 儲存圓形圖片
    circular_image.save(output_path, format="PNG")

# 使用範例
input_image_path = "./static/image/screenShot.jpg"
output_image_path = "./static/image/circle.png"

crop_to_square_and_circle(input_image_path, output_image_path)


name_classes    = ['wafer_pie', 'oreo', 'yuki', 'snow_cracker', 'rice_cracker', 'rye_biscuit']
# Read merged data from the text file
read_merged_list = []
# Read data from 'merged_data.txt'
with open('./static/file/merged_data.txt', 'r') as file:
    read_merged_list = [list(map(float, line.strip().split(','))) for line in file]
# print(read_merged_list)

data = []
total = [0.0, 0.0, 0.0, 0.0, 0.0]
for i in range(len(name_classes)):
    if read_merged_list[i][0] == 0:
        continue
    data.append([name_classes[i]] + read_merged_list[i])
    for j in range(len(read_merged_list[i])):
        total[j] += read_merged_list[i][j]
        total[j] = round(total[j], 3)


# print(total)
data.append(['Total'] + total)
read_merged_list.clear()
# print(data)


# 建立環圈圖
# matplotlib.rc('font', family='Microsoft JhengHei')
matplotlib.rc('font', family='Comic Sans MS')
labels = ['Protein','Carbohydrate','Fat']
sizes = total[-3:]
print(sizes)
# colors = ['gold', 'yellowgreen', 'lightcoral']
colors = ['#ffbc7d', '#a6e390', '#63cbf8']
explode = (0.05, 0.05, 0.05)
current_time = datetime.now()
# 創建環圈圖
fig, ax = plt.subplots()
ax.set_aspect('equal')  # 確保軸的長寬比相等
_, texts, _ = ax.pie(sizes,
                    explode=explode,
                    labels=labels,
                    colors=colors,
                    autopct='%1.2f%%',
                    pctdistance=0.7,
                    radius=1.5,
                    textprops={'color': 'black', 'weight': 'bold', 'size': 10})
# 隱藏外側的標籤
for text in texts:
    text.set_visible(False)

# # 把圓餅圖中間加上一個圓，就可變成環圈圖
# # circle = plt.Circle((0, 0), 0.70, fc='#eaeaea')
    
# 將圓形轉換為圖片
circle_image_path = './static/image/circle.png'
circle_image = plt.imread(circle_image_path)
circle_image = OffsetImage(circle_image, zoom=0.25)
ab_circle = AnnotationBbox(circle_image, (0.5, 0.5), frameon=False, xycoords='axes fraction', boxcoords='axes fraction')
ax.add_artist(ab_circle)

# 加上圖例
ax.legend(labels, bbox_to_anchor=(0.2, 0), loc="right")
# 確保圖表繪製為具有相等長寬比的圓形
ax.axis('equal')
# 加上標題 -- 詳細營養資訊圖
ax.set_title('Detailed Nutritional Information Chart')
# 加入圖標
icon_path = './static/image/logo_removebg.png'
icon = plt.imread(icon_path)
icon_image = OffsetImage(icon, zoom=0.2)
ab = AnnotationBbox(icon_image, (0, 1), frameon=False, xycoords='axes fraction', boxcoords='axes fraction')
ax.add_artist(ab)
# 添加日期時間到圖片中央底部
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
ax.text(0, -1.9, f"Generated on: {formatted_time}", ha='center', va='center', fontsize=10, color='black')
# 在右下角加上總熱量
text_to_add = f"Total Calories :\n{total[2]} cal(s)"
ax.text(2.5, -1.95, text_to_add, fontsize=14, va='bottom', ha='right', color='black')

# 儲存圖片
plt.savefig('donut_chart_seller.png', transparent=True)





# if len(data) >15:
#     lenData = (len(data)-1)/2-1
# else:
#     lenData = (len(data)-1)/2+1
# table_height = lenData
# print(len(data))
# print(table_height)

# fig, ax2 = plt.subplots(figsize=(8, table_height))
# col_labels = ['foods', 'Weight(g)', 'Calories(cal)', 'Protein(g)', 'Carbohydrates(g)', 'Fat(g)']

# # Hide axes
# ax2.axis('off')
# # ax2.axis('tight')

# # Change background color
# fig.patch.set_facecolor('xkcd:light grey')
# # ax2.set_facecolor('xkcd:light grey')

# # Table from data
# table = ax2.table(cellText=data, colLabels=col_labels, cellLoc='center', loc='center')

# # Make col_labels (table headers) bold
# for (i, label) in enumerate(col_labels):
#     table[0, i].get_text().set_fontweight('bold')

# # Change cell color
# cells = table.properties()["children"]
# i = 0
# for cell in cells:
#     # cell.set_facecolor('xkcd:light blue')
#     if i % 2 == 0:
#         cell.set_facecolor('#AEDFE0')  # Set even rows color
#     else:
#         cell.set_facecolor('#a6e390')  # Set odd rows color
#     i += 1
#     cell.set_edgecolor('white')


# # Adjust column widths
# table.auto_set_column_width(col=list(range(len(col_labels))))
# table.auto_set_font_size(False)
# table.set_fontsize(10)
# table.scale(1, 2)  # change the second parameter to adjust row height

# plt.savefig('./static/image/sheet_img.png', transparent=True)








