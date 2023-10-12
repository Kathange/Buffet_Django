from django.contrib import admin
# 從models.py 新增class路徑
# 後方新增 你所建立的 "類別名稱"，這裡我的名稱是BuffetCaloriesAdmin
# 這樣才可以在網頁上有資料庫管理的介面
from .models import BuffetCalories, BuffetCaloriesAdmin
from .models import UnpopularFoods, UnpopularFoodsAdmin


# Register your models here.

# 將管理者類別 BuffetCaloriesAdmin 填至該類別後方
# (此處只要在創建資料庫table之後執行一次即可，之後請反白，不然會出錯)
# admin.site.register(BuffetCalories, BuffetCaloriesAdmin)
# admin.site.register(UnpopularFoods, UnpopularFoodsAdmin)
