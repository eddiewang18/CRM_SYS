# Generated by Django 3.2 on 2023-05-18 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_data', '0010_vipinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vipinfo',
            name='black',
            field=models.BooleanField(db_column='black', default=False, verbose_name='黑名單'),
        ),
    ]
