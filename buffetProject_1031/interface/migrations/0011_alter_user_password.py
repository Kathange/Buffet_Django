# Generated by Django 4.2.3 on 2023-10-30 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0010_detail_record_calorie_detail_record_carbohydrate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]