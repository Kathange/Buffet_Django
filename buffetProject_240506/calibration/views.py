from django.shortcuts import render
from django.http.response import StreamingHttpResponse

from ._3D_Ccamera import FoodVedioCameraCalib
from interface.models import provide_food

# Create your views here.

# 設置 camera (要把模型放進去應該去camera.py寫)
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# 連接攝影機(特定語法，應該，我是複製貼上)，gen(camera.py中的class)
def FoodVedioFeedCalib(request):
    return StreamingHttpResponse(gen(FoodVedioCameraCalib()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

# 校正空盤的頁面
def calib(request):
    return render(request, 'calibration\\calib.html')

def analysis(request):
    provide = provide_food.objects.all()
    return render(request, 'calibration\\analysis.html', {'provide' : provide})