# Generated by Django 3.2 on 2023-06-15 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_data', '0017_alter_product_prod_name'),
        ('label_data', '0014_auto_20230615_1527'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vip_label',
            unique_together={('label_gid', 'label_name')},
        ),
        migrations.AlterUniqueTogether(
            name='vip_label_group',
            unique_together={('cpnyid', 'label_gname')},
        ),
    ]
