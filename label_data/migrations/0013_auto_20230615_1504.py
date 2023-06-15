# Generated by Django 3.2 on 2023-06-15 07:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label_data', '0012_auto_20230612_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales00',
            name='input_date',
            field=models.DateField(db_column='input_date', default=datetime.date(2023, 6, 15), verbose_name='入賬(消費)日期'),
        ),
        migrations.AlterField(
            model_name='vip_label',
            name='label_name',
            field=models.CharField(db_column='label_name', max_length=50, verbose_name='標籤名稱'),
        ),
        migrations.AlterField(
            model_name='vip_label_group',
            name='label_gname',
            field=models.CharField(db_column='label_gname', max_length=50, verbose_name='標籤群組名稱'),
        ),
    ]
