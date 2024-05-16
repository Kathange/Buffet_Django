from django.http import JsonResponse
from matplotlib import pyplot as plt
import io
import base64

def generate_chart(request):
    selected_date = request.GET.get('date')
    selected_food = request.GET.get('food')
    chart_type = request.GET.get('chart_type')
    custom_chart = request.GET.get('custom_chart')
    
    fig, ax = plt.subplots()
    if custom_chart == 'sales':
        ax.plot([1, 2, 3, 4], [10, 20, 15, 25])  # 示例销售量图表
        ax.set_title(f"Sales Chart for {selected_food} on {selected_date}")
    elif custom_chart == 'profit':
        ax.plot([1, 2, 3, 4], [5, 15, 10, 20])  # 示例利润图表
        ax.set_title(f"Profit Chart for {selected_food} on {selected_date}")
    elif chart_type == 'line':
        ax.plot([1, 2, 3, 4], [10, 20, 25, 30])  # 示例线图
        ax.set_title(f"Line Chart for {selected_food} on {selected_date}")
    elif chart_type == 'bar':
        ax.bar([1, 2, 3, 4], [10, 20, 25, 30])  # 示例柱状图
        ax.set_title(f"Bar Chart for {selected_food} on {selected_date}")
    elif chart_type == 'scatter':
        ax.scatter([1, 2, 3, 4], [10, 20, 25, 30])  # 示例散点图
        ax.set_title(f"Scatter Chart for {selected_food} on {selected_date}")
    else:
        # 默认圆圈图表，显示今日销售总额
        today_sales = 10000  # 示例数据，应从数据库中获取实际数据
        ax.pie([1], labels=[f"${today_sales}"], startangle=90, counterclock=False, wedgeprops=dict(width=0.3))
        ax.set_title(f"Today's Total Sales: ${today_sales}")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    
    return JsonResponse({'image_base64': image_base64, 'selected_date': selected_date, 'selected_food': selected_food})