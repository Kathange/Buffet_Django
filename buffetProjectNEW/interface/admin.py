from django.contrib import admin
# 後方新增 你所建立的 "類別名稱"，這裡我的名稱是BuffetCaloriesAdmin
from .models import BuffetCalories, BuffetCaloriesAdmin
from .models import UnpopularFoods, UnpopularFoodsAdmin


# Register your models here.

# 將管理者類別 BuffetCaloriesAdmin 填至該類別後方
# admin.site.register(BuffetCalories, BuffetCaloriesAdmin)
# admin.site.register(UnpopularFoods, UnpopularFoodsAdmin)
