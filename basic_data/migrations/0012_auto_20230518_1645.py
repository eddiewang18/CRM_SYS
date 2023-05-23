# Generated by Django 3.2 on 2023-05-18 08:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('basic_data', '0011_alter_vipinfo_black'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vipinfo',
            name='apply_date',
            field=models.DateField(db_column='apply_date', default=django.utils.timezone.now, verbose_name='申請日期'),
        ),
        migrations.AlterField(
            model_name='vipinfo',
            name='vipinfo_group_id',
            field=models.ForeignKey(blank=True, db_column='vipinfo_group_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='basic_data.vipinfo_group', verbose_name='會員群組'),
        ),
    ]