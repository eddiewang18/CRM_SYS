# Generated by Django 3.2 on 2023-05-11 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_data', '0005_auto_20230504_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='HRUSER_GROUP',
            fields=[
                ('group_id', models.CharField(db_column='group_id', max_length=10, primary_key=True, serialize=False, verbose_name='員工群組編號')),
                ('group_name', models.CharField(db_column='group_name', max_length=20, verbose_name='員工群組名稱')),
                ('cuser', models.CharField(db_column='cuser', max_length=20, verbose_name='創始人')),
                ('cdate', models.DateField(auto_now_add=True, db_column='cdate', verbose_name='創立日期')),
                ('ctime', models.TimeField(auto_now_add=True, db_column='ctime', verbose_name='創立時間')),
                ('muser', models.CharField(db_column='muser', max_length=20, verbose_name='異動者')),
                ('mdate', models.DateField(auto_now=True, db_column='mdate', verbose_name='異動日期')),
                ('mtime', models.TimeField(auto_now=True, db_column='mtime', verbose_name='異動時間')),
            ],
            options={
                'db_table': 'HRUSER_GROUP',
            },
        ),
    ]
