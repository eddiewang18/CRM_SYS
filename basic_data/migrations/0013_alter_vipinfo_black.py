# Generated by Django 3.2 on 2023-05-20 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_data', '0012_auto_20230518_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vipinfo',
            name='black',
            field=models.BooleanField(db_column='black', verbose_name='黑名單'),
        ),
    ]
