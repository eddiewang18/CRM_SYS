# Generated by Django 3.2 on 2023-06-10 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_data', '0017_alter_product_prod_name'),
        ('label_data', '0007_sales00_input_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale01',
            name='sales_sno',
            field=models.CharField(db_column='sales_sno', default='', max_length=30, verbose_name='交易明細序號'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sale01',
            name='sale01_id',
            field=models.CharField(db_column='sale01_id', max_length=30, primary_key=True, serialize=False),
        ),
        migrations.AlterUniqueTogether(
            name='sale01',
            unique_together={('sale00_id', 'sales_sno', 'prod_id')},
        ),
    ]