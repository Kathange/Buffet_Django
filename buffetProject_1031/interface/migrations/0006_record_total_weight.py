# Generated by Django 4.2.3 on 2023-10-29 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0005_food_info_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='total_weight',
            field=models.DecimalField(decimal_places=3, default=1, max_digits=7),
            preserve_default=False,
        ),
    ]
