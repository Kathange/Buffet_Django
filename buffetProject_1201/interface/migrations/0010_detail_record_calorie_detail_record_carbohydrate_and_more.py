# Generated by Django 4.2.3 on 2023-10-29 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0009_alter_food_info_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail_record',
            name='calorie',
            field=models.DecimalField(decimal_places=3, default=1, max_digits=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detail_record',
            name='carbohydrate',
            field=models.DecimalField(decimal_places=3, default=1, max_digits=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detail_record',
            name='fat',
            field=models.DecimalField(decimal_places=3, default=1, max_digits=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detail_record',
            name='protein',
            field=models.DecimalField(decimal_places=3, default=1, max_digits=7),
            preserve_default=False,
        ),
    ]
