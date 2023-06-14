# Generated by Django 3.2 on 2023-06-10 01:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label_data', '0006_sale01_sales00'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales00',
            name='input_date',
            field=models.DateField(db_column='input_date', default=datetime.date(2023, 6, 10), verbose_name='入賬(消費)日期'),
        ),
    ]