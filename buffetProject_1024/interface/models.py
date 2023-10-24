from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# 更新新創建的資料庫讓其可以顯示在admin網頁中，需要在cmd中打入下面兩行
# python manage.py makemigrations
# python manage.py migrate

# Create your models here.
# 食物名字
# 一份=體積
# 一份有多少熱量
# 一份有多少營養素(占比%數)
# class BuffetCalories(models.Model):
#     food_name = models.CharField(max_length=30)
#     food_volume = models.DecimalField(max_digits=6, decimal_places=3)
#     food_calories = models.DecimalField(max_digits=6, decimal_places=3)
    # 營養素先略過?

    # 覆寫 __str__  (增加資料易讀性)
    # 意思是如果我有別的table需要foreign key連到此table，那麼在別的table上就只會顯示food_name
    # def __str__(self):
    #     return self.food_name
        # return f"{self.food_name}, {self.food_volume}, {self.food_calories}"

# 自訂 資料排序方式 或 顯示隱藏資料
# @admin.register(BuffetCalories)
# class BuffetCaloriesAdmin(admin.ModelAdmin):
#     # 列出全部資訊
#     list_display = [field.name for field in BuffetCalories._meta.fields]
#     # 搜尋欄位
#     search_fields = ('food_name', 'food_calories')
#     # id 由小到大 排序
#     ordering = ('id', )



# # 後面兩個table同理


# class UnpopularFoods(models.Model):
#     volume_sum = models.DecimalField(max_digits=8, decimal_places=3)
#     item_name = models.ForeignKey(BuffetCalories, null=True, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.item_name}, {self.volume_sum}"

# @admin.register(UnpopularFoods)
# class UnpopularFoodsAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in UnpopularFoods._meta.fields]
#     ordering = ('id', )



# class Member(models.Model):
#     account = models.CharField(max_length=30)
#     password = models.CharField(max_length=30)

#     def __str__(self):
#         return self.account

# @admin.register(Member)
# class MemberAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Member._meta.fields]
#     ordering = ('id', )



# class provide_food(models.Model):
#     name = models.CharField(max_length=100, primary_key=True)
    
#     class Meta:
#         db_table: 'provide_food'

#     def __str__(self):
#          return self.name
# # @admin.register(provide_food)
# # class prvide_food_admin(admin.ModelAdmin):
# #     list_display = [field.name for field in provide_food._meta.fields]
# #     ordering = ('id', )

# class food_code(models.Model):
#     food_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100, null=False, blank=False)

#     class Meta:
#         db_table: 'food_code'

# class food_info(models.Model):
#     food_id = models.IntegerField(primary_key=True)
#     weight = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
#     calorie = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
#     protein = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
#     carbohydrate = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
#     fat = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)

#     class Meta:
#         db_table: 'food_info'

# class user(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     account = models.CharField(max_length=100, null=False, blank=False)
#     password = models.CharField(max_length=100, null=False, blank=False)
#     customer = models.BooleanField(default=True, null=False, blank=False)

#     class Meta:
#         db_table: 'user'

# class record(models.Model):
#     record_id = models.AutoField(primary_key=True, unique=True)
#     seller_id = models.ForeignKey(user, to_field='user_id', on_delete=models.RESTRICT, related_name="fk_record_sellerId")
#     user_id = models.ForeignKey(user, to_field='user_id', on_delete=models.RESTRICT, related_name="fk_reocrd_userId")
#     eat_date = models.DateField(null=False, blank=False)
#     eat_time = models.TimeField(null=False, blank=False)
#     food_img = models.BinaryField(null=False, blank=False)
#     total_cal = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
#     total_pro = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
#     total_carbo = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
#     total_fat = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
#     cost = models.PositiveIntegerField(null=False, blank=False)

#     class Meta:
#         db_table: 'record'

# class detail_record(models.Model):
#     record_id = models.ForeignKey(record, primary_key=True, to_field='record_id', on_delete=models.RESTRICT, related_name='fk_detailRecord_recordId')
#     # user_id = models.ForeignKey(record, to_field='user_id', on_delete=models.RESTRICT, related_name='fk_detailRecord_userId')
#     # eat_date = models.ForeignKey(record, to_field='eat_date', on_delete=models.RESTRICT, related_name='fk_detailRecord_eatDate')
#     # eat_time = models.ForeignKey(record, to_field='eat_time', on_delete=models.RESTRICT, related_name='fk_detailRecord_eatTime')
#     food_id = models.ForeignKey(food_code, to_field='food_id', on_delete=models.RESTRICT, related_name='fk_detailRecord_foodId')
#     weight = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)

#     def __str__(self):
#         return f"{self.food_id}, {self.record_id}"
    

#     class Meta:
#         db_table: 'detail_record'
class food_code(models.Model):
    food_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    class Meta:
        db_table: 'food_code'


class provide_food(models.Model):
    # name = models.CharField(max_length=100, primary_key=True)
    name = models.ForeignKey(food_code, primary_key=True, to_field='name', on_delete=models.RESTRICT, related_name='fk_prvideFood_name')
    
    class Meta:
        db_table: 'provide_food'


class food_info(models.Model):
    # food_id = models.IntegerField(primary_key=True)
    food_id = models.ForeignKey(food_code, primary_key=True, to_field='food_id', on_delete=models.RESTRICT, related_name='fk_foodInfo_foodId')
    weight = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
    calorie = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
    protein = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
    carbohydrate = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
    fat = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)

    class Meta:
        db_table: 'food_info'


class user(models.Model):
    user_id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False, unique=True)
    customer = models.BooleanField(default=True, null=False, blank=False)

    class Meta:
        db_table: 'user'
    def __str__(self):
        # return self.account
        return f"{self.user_id}, {self.account}, {self.password}, {self.customer}"


class record(models.Model):
    record_id = models.AutoField(primary_key=True)
    seller_id = models.ForeignKey(user, to_field='user_id', on_delete=models.RESTRICT, related_name="fk_record_sellerId")
    user_id = models.ForeignKey(user, to_field='user_id', on_delete=models.RESTRICT, related_name="fk_reocrd_userId")
    eat_date = models.DateField(null=False, blank=False)
    eat_time = models.TimeField(null=False, blank=False)
    food_img = models.BinaryField(null=False, blank=False)
    total_cal = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
    total_pro = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
    total_carbo = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
    total_fat = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)
    cost = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        db_table: 'record'


class detail_record(models.Model):
    record_id = models.ForeignKey(record, primary_key=True, to_field='record_id', on_delete=models.RESTRICT, related_name='fk_detailRecord_recordId')
    # user_id = models.ForeignKey(record, to_field='user_id', on_delete=models.RESTRICT, related_name='fk_detailRecord_userId')
    # eat_date = models.ForeignKey(record, to_field='eat_date', on_delete=models.RESTRICT, related_name='fk_detailRecord_eatDate')
    # eat_time = models.ForeignKey(record, to_field='eat_time', on_delete=models.RESTRICT, related_name='fk_detailRecord_eatTime')
    food_id = models.ForeignKey(food_code, to_field='food_id', on_delete=models.RESTRICT, related_name='fk_detailRecord_foodId')
    weight = models.DecimalField(max_digits=7, decimal_places=3, null=False, blank=False)

    # def __str__(self):
    #     return f"{self.record_id}, {self.food_id}"
    
    class Meta:
        db_table: 'detail_record'
        unique_together = ('record_id', 'food_id')
