from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# 更新新創建的資料庫讓其可以顯示在admin網頁中
# python manage.py makemigrations
# python manage.py migrate

# Create your models here.
# 食物名字
# 一份=體積
# 一份有多少熱量
# 一份有多少營養素(占比%數)
class BuffetCalories(models.Model):
    food_name = models.CharField(max_length=30)
    food_volume = models.DecimalField(max_digits=6, decimal_places=3)
    food_calories = models.DecimalField(max_digits=6, decimal_places=3)
    # 營養素先略過?

    # 覆寫 __str__  (增加資料易讀性)
    def __str__(self):
        return self.food_name
        # return f"{self.food_name}, {self.food_volume}, {self.food_calories}"

@admin.register(BuffetCalories)
class BuffetCaloriesAdmin(admin.ModelAdmin):
    # 列出全部資訊
    list_display = [field.name for field in BuffetCalories._meta.fields]
    # 搜尋欄位
    search_fields = ('food_name', 'food_calories')
    # id 由小到大 排序
    ordering = ('id', )



class UnpopularFoods(models.Model):
    volume_sum = models.DecimalField(max_digits=8, decimal_places=3)
    item_name = models.ForeignKey(BuffetCalories, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item_name}, {self.volume_sum}"

@admin.register(UnpopularFoods)
class UnpopularFoodsAdmin(admin.ModelAdmin):
    # 列出全部資訊
    list_display = [field.name for field in UnpopularFoods._meta.fields]
    # id 由小到大 排序
    ordering = ('id', )



class Member(models.Model):
    account = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.account

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    # 列出全部資訊
    list_display = [field.name for field in Member._meta.fields]
    # id 由小到大 排序
    ordering = ('id', )




