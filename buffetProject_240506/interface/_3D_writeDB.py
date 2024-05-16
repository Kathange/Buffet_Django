"""

此為辨識結束後，將相關資料寫進資料庫中
寫進資料庫的資料包括：歷史記錄(record), 詳細營養資訊(detail_record)

"""


from .models import user, record, detail_record, food_code
from datetime import datetime
from io import BytesIO
import requests
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image, ImageDraw
matplotlib.use('Agg')

name_classes    = ['wafer_pie', 'oreo', 'yuki', 'snow_cracker', 'rice_cracker', 'rye_biscuit']
# ch_name_classes = ['新貴派','oreo','yuki','雪餅','旺旺仙貝','黑麥口糧']
imgur_token = '412b87ea68ecab734b84985d38a425f5e56623e1'

def upload_food_image(img_path, imgur_token):
    headers = {
        'Authorization': f'Bearer {imgur_token}',
    }
    # 將照片讀取為二進制數據
    with open(img_path, 'rb') as img_file:
        img_data = img_file.read()
    # 設定上傳的 URL
    upload_url = 'https://api.imgur.com/3/upload'
    # 設定上傳的參數
    upload_params = {
        'image': img_data,
    }
    # 發送 POST 請求進行上傳
    response = requests.post(upload_url, headers=headers, files=upload_params)
    # 解析 API 回應
    if response.status_code == 200:
        data = response.json()
        link = data['data']['link']
        print(f'照片上傳成功！連結：{link}')
        return link
    else:
        print(f'照片上傳失敗。錯誤碼：{response.status_code}')
        return None


def upload_image(img_data, imgur_token):
    headers = {'Authorization': f'Bearer {imgur_token}',}
    # 設定上傳的 URL
    upload_url = 'https://api.imgur.com/3/upload'
    # 設定上傳的參數
    upload_params = {
        'image': img_data.getvalue(),
    }
    # 發送 POST 請求進行上傳
    response = requests.post(upload_url, headers=headers, files=upload_params)
    # 解析 API 回應
    if response.status_code == 200:
        data = response.json()
        link = data['data']['link']
        print(f'照片上傳成功！連結：{link}')
        # 回傳 Imgur 照片的連結
        return link
    else:
        print(f'照片上傳失敗。錯誤碼：{response.status_code}')
        return None


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


def generateDountChartAndSheet(data, total, current_time):
    # 建立環圈圖
    # matplotlib.rc('font', family='Microsoft JhengHei')
    matplotlib.rc('font', family='Comic Sans MS')
    labels = ['Protein','Carbohydrate','Fat']
    sizes = total[-3:]
    print(sizes)
    # colors = ['gold', 'yellowgreen', 'lightcoral']
    colors = ['#ffbc7d', '#a6e390', '#63cbf8']
    explode = (0.05, 0.05, 0.05)
    # current_time = datetime.now()
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
    text_to_add = f"Total Calories :\n{total[1]} cal(s)"
    ax.text(2.5, -1.95, text_to_add, fontsize=14, va='bottom', ha='right', color='black')
    # 儲存圖片
    plt.savefig('./static/image/donut_chart_seller.png', transparent=True)
    
    # 儲存到緩衝區
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    # 上傳照片並獲取 Imgur 照片的連結
    imgur_dc_link = upload_image(buffer, imgur_token)
    if imgur_dc_link:
        print(f'Imgur 照片的連結為：{imgur_dc_link}')
    plt.clf()


    # 創建表格
    if len(data) >15:
        lenData = (len(data)-1)/2-1
    else:
        lenData = (len(data)-1)/2+1
    table_height = lenData
    print(len(data))
    print(table_height)

    fig, ax2 = plt.subplots(figsize=(8, table_height))
    col_labels = ['foods', 'Weight(g)', 'Calories(cal)', 'Protein(g)', 'Carbohydrates(g)', 'Fat(g)']

    # Hide axes
    ax2.axis('off')
    # ax2.axis('tight')

    # Change background color
    fig.patch.set_facecolor('xkcd:light grey')
    # ax2.set_facecolor('xkcd:light grey')

    # Table from data
    table = ax2.table(cellText=data, colLabels=col_labels, cellLoc='center', loc='center')

    # Make col_labels (table headers) bold
    for (i, label) in enumerate(col_labels):
        table[0, i].get_text().set_fontweight('bold')

    # Change cell color
    cells = table.properties()["children"]
    i = 0
    for cell in cells:
        # cell.set_facecolor('xkcd:light blue')
        if i % 2 == 0:
            cell.set_facecolor('#AEDFE0')  # Set even rows color
        else:
            cell.set_facecolor('#a6e390')  # Set odd rows color
        i += 1
        cell.set_edgecolor('white')


    # Adjust column widths
    table.auto_set_column_width(col=list(range(len(col_labels))))
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)  # change the second parameter to adjust row height

    plt.savefig('./static/image/sheet_img.png', transparent=True)


    # 儲存到緩衝區
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    # 上傳照片並獲取 Imgur 照片的連結
    imgur_sheet_link = upload_image(buffer, imgur_token)
    if imgur_sheet_link:
        print(f'Imgur 照片的連結為：{imgur_sheet_link}')
    plt.clf()
    return imgur_dc_link, imgur_sheet_link


def writeDB():     
    # 拿取詳細資訊，show:單一品項詳細資訊 ; total:總詳細資訊
    read_merged_list = []
    with open('./static/file/merged_data.txt', 'r') as file:
        read_merged_list = [list(map(float, line.strip().split(','))) for line in file]
    show = []
    total = [0.0, 0.0, 0.0, 0.0, 0.0]
    for i in range(len(name_classes)):
        if read_merged_list[i][0] == 0:
            continue
        show.append([name_classes[i]] + read_merged_list[i])
        for j in range(len(read_merged_list[i])):
            total[j] += read_merged_list[i][j]
            total[j] = round(total[j], 3)
    data = show.copy()
    data.append(['Total'] + total)


    # 拿取時間
    current_time = datetime.now()

    # 生成circle.png放到環圈圖中
    input_image_path = "./static/image/screenShot.jpg"
    output_image_path = "./static/image/circle.png"
    crop_to_square_and_circle(input_image_path, output_image_path)
        
    dc_img, sheet_img = generateDountChartAndSheet(data, total, current_time)
    
    image_path = './static/image/screenShot.jpg'
    food_img = upload_food_image(image_path, imgur_token)

    # 拿取價錢
    volume_data = []
    with open('./static/file/volume.txt', 'r') as file:
        volume_data = [list(map(float, line.strip().split(','))) for line in file]
    cost = int(round(volume_data[0][0], 0))
    # 获取日期部分
    date_part = current_time.date()
    # 获取时间部分
    time_part = current_time.time()
    # 知道現在有多少筆資料
    # data_count = record.objects.count()
    # 讀取照片檔
    # with open('./static/image/screenShot.jpg', 'rb') as photo_file:
    #     photo_binary_data = photo_file.read()
    # 讀取RFID
    with open('./static/file/rfid.txt', 'r') as file:
        rfid_data = file.read()
    
    # 拿取UFID的主人的id -- 
    buyer = user.objects.get(user_RFID=rfid_data)
    # 寫入 record 資料庫
    # recordunit = record.objects.create(record_id=data_count+1, user_id=buyer, eat_date=date_part, eat_time=time_part, food_img=food_img, total_weight=total[0], total_cal=total[1], total_pro=total[2], total_carbo=total[3], total_fat=total[4], cost=cost, donut_chart_img=dc_img, sheet_img=sheet_img)
    recordunit = record.objects.create(user_line=buyer, eat_date=date_part, eat_time=time_part, food_img=food_img, total_weight=total[0], total_cal=total[1], total_pro=total[2], total_carbo=total[3], total_fat=total[4], cost=cost, donut_chart_img=dc_img, sheet_img=sheet_img)
    recordunit.save()

    flask_url = "https://a967-211-72-73-205.ngrok-free.app/newRecord"
    # print(type(uid_value))
    response = requests.post(flask_url, data={'new_record':"1"})
    if response.status_code == 200:
        print('success')
    else:
        print('failed', response.status_code)
    
    for item in show:
        # Assuming you have the related food objects in foods_with_provide_food
        food_object = food_code.objects.get(name=item[0], fk_prvideFood_name__isnull=False)
        print(food_object)
        if not detail_record.objects.filter(food_id=food_object, record_id=recordunit).exists():
            DRunit = detail_record.objects.create(record_id=recordunit, food_id=food_object, weight=item[1], calorie=item[2], protein=item[3], carbohydrate=item[4], fat=item[5]) 
            # DRunit.save()
            print("save")
        else:
            print("not save")
    return None

