from django.shortcuts import render

# Create your views here.
def buyer(request):
    # 因為'\b'為跳脫字元，所以要'\'存在，要再加一個'\'跳脫
    return render(request, 'interface\\buyer.html')

