# Generated by Django 3.2 on 2023-05-31 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label_data', '0003_vip_label_group_formula_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formula',
            name='cpnyid',
        ),
        migrations.AlterField(
            model_name='formula',
            name='formula_id',
            field=models.CharField(db_column='formula_id', max_length=25, primary_key=True, serialize=False, verbose_name='公式編號'),
        ),
    ]
