# Generated by Django 3.2 on 2023-06-12 13:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label_data', '0011_auto_20230611_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales00',
            name='input_date',
            field=models.DateField(db_column='input_date', default=datetime.date(2023, 6, 12), verbose_name='入賬(消費)日期'),
        ),
        migrations.AlterField(
            model_name='vip_label_group',
            name='xor',
            field=models.CharField(choices=[('0', '允許選擇多標籤'), ('1', '僅能選擇單一標籤')], db_column='isxor', default='1', max_length=2, verbose_name='貼標時客人是否可以擁有群組內一個以上的標籤'),
        ),
    ]
