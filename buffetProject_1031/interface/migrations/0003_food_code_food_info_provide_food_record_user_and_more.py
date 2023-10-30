# Generated by Django 4.2.3 on 2023-10-23 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0002_unpopularfoods'),
    ]

    operations = [
        migrations.CreateModel(
            name='food_code',
            fields=[
                ('food_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='food_info',
            fields=[
                ('food_id', models.IntegerField(primary_key=True, serialize=False)),
                ('weight', models.DecimalField(decimal_places=3, max_digits=7)),
                ('calorie', models.DecimalField(decimal_places=3, max_digits=7)),
                ('protein', models.DecimalField(decimal_places=3, max_digits=7)),
                ('carbohydrate', models.DecimalField(decimal_places=3, max_digits=7)),
                ('fat', models.DecimalField(decimal_places=3, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='provide_food',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='record',
            fields=[
                ('record_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('eat_date', models.DateField()),
                ('eat_time', models.TimeField()),
                ('food_img', models.BinaryField()),
                ('total_cal', models.DecimalField(decimal_places=3, max_digits=7)),
                ('total_pro', models.DecimalField(decimal_places=3, max_digits=7)),
                ('total_carbo', models.DecimalField(decimal_places=3, max_digits=7)),
                ('total_fat', models.DecimalField(decimal_places=3, max_digits=7)),
                ('cost', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('account', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('customer', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='unpopularfoods',
            name='item_name',
        ),
        migrations.CreateModel(
            name='detail_record',
            fields=[
                ('record_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, primary_key=True, related_name='fk_detailRecord_recordId', serialize=False, to='interface.record')),
                ('weight', models.DecimalField(decimal_places=3, max_digits=7)),
                ('food_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='fk_detailRecord_foodId', to='interface.food_code')),
            ],
        ),
        migrations.DeleteModel(
            name='BuffetCalories',
        ),
        migrations.DeleteModel(
            name='UnpopularFoods',
        ),
        migrations.AddField(
            model_name='record',
            name='seller_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='fk_record_sellerId', to='interface.user'),
        ),
        migrations.AddField(
            model_name='record',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='fk_reocrd_userId', to='interface.user'),
        ),
    ]
