# Generated by Django 3.2 on 2023-05-13 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic_data', '0007_crm_hruser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crm_hruser',
            name='shop_id',
            field=models.ForeignKey(db_column='shop_id', default='', on_delete=django.db.models.deletion.CASCADE, to='basic_data.shop', verbose_name='歸屬分店'),
            preserve_default=False,
        ),
    ]
