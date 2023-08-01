from django.db import models
from django.contrib import admin
# from django.utils.translation import gettext_lazy as _

# Create your models here.
# 食物名字
# 一份=體積
# 一份有多少熱量
# 一份有多少營養素(占比%數)
class BuffetCalories(models.Model):
    food_name = models.CharField(max_length=30)
    grip_volume = models.DecimalField(max_digits=6, decimal_places=3)
    food_calories = models.DecimalField(max_digits=6, decimal_places=3)
    # 營養素先略過?
    # 食物名稱要用中文嗎?

    # 覆寫 __str__  (增加資料易讀性)
    def __str__(self):
        return self.food_name
