# Generated by Django 3.2 on 2023-06-15 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label_data', '0015_auto_20230615_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vip_label',
            name='cuser',
            field=models.CharField(db_column='cuser', default='admin', max_length=20, verbose_name='創始人'),
        ),
        migrations.AlterField(
            model_name='vip_label',
            name='muser',
            field=models.CharField(db_column='muser', default='admin', max_length=20, verbose_name='異動者'),
        ),
    ]