# Generated by Django 3.2 on 2023-06-10 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label_data', '0009_paramater_stat_paramater_stat_company_vip_formula_stat_vip_label_stat'),
    ]

    operations = [
        migrations.AddField(
            model_name='formula',
            name='formula_note',
            field=models.CharField(db_column='formula_note', max_length=150, null=True, verbose_name='公式中文規則'),
        ),
    ]
