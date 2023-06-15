# Generated by Django 3.2 on 2023-06-15 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label_data', '0013_auto_20230615_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='vip_label',
            name='sys_create',
            field=models.CharField(blank=True, db_column='sys_create', max_length=2, null=True, verbose_name='系統預設創建標籤'),
        ),
        migrations.AddField(
            model_name='vip_label_group',
            name='sys_create',
            field=models.CharField(blank=True, db_column='sys_create', max_length=2, null=True, verbose_name='系統預設創建標籤'),
        ),
        migrations.AlterField(
            model_name='vip_label_group',
            name='cuser',
            field=models.CharField(db_column='cuser', default='admin', max_length=20, verbose_name='創始人'),
        ),
        migrations.AlterField(
            model_name='vip_label_group',
            name='muser',
            field=models.CharField(db_column='muser', default='admin', max_length=20, verbose_name='異動者'),
        ),
    ]
