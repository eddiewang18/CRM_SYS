# Generated by Django 3.2 on 2023-05-31 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic_data', '0016_product_producttype'),
        ('label_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paramater',
            fields=[
                ('param_id', models.CharField(db_column='param_id', max_length=50, primary_key=True, serialize=False, verbose_name='參數編號')),
                ('param_name', models.CharField(db_column='param_name', max_length=50, unique=True, verbose_name='參數名稱')),
                ('param_unit', models.CharField(choices=[('0', '其它'), ('1', '日期'), ('2', '天'), ('3', '次'), ('4', '元'), ('5', '百分比')], db_column='param_unit', max_length=3, verbose_name='參數單位')),
                ('descr', models.CharField(db_column='descr', max_length=200, verbose_name='公式說明')),
                ('is_brand', models.CharField(choices=[('Y', '是'), ('N', '否')], db_column='is_brand', max_length=2, verbose_name='判斷是否為品牌變數')),
            ],
            options={
                'db_table': 'Paramater',
            },
        ),
        migrations.CreateModel(
            name='VIP_LABEL',
            fields=[
                ('label_id', models.CharField(db_column='label_id', max_length=50, primary_key=True, serialize=False, verbose_name='標籤代號')),
                ('label_name', models.CharField(db_column='label_name', max_length=50, unique=True, verbose_name='標籤名稱')),
                ('calmin', models.DecimalField(db_column='calmin', decimal_places=2, max_digits=10, verbose_name='計算區間起')),
                ('calmax', models.DecimalField(db_column='calmax', decimal_places=2, max_digits=10, verbose_name='計算區間迄')),
                ('label_enable', models.CharField(choices=[('0', '否'), ('1', '是')], db_column='label_enable', default='0', max_length=2, verbose_name='是否停用')),
                ('cuser', models.CharField(db_column='cuser', max_length=20, verbose_name='創始人')),
                ('cdate', models.DateField(auto_now_add=True, db_column='cdate', verbose_name='創立日期')),
                ('ctime', models.TimeField(auto_now_add=True, db_column='ctime', verbose_name='創立時間')),
                ('muser', models.CharField(db_column='muser', max_length=20, verbose_name='異動者')),
                ('mdate', models.DateField(auto_now=True, db_column='mdate', verbose_name='異動日期')),
                ('mtime', models.TimeField(auto_now=True, db_column='mtime', verbose_name='異動時間')),
                ('label_gid', models.ForeignKey(db_column='label_gid', on_delete=django.db.models.deletion.CASCADE, to='label_data.vip_label_group', verbose_name='標籤群組代號')),
            ],
            options={
                'db_table': 'VIP_LABEL',
            },
        ),
        migrations.CreateModel(
            name='Formula',
            fields=[
                ('formula_id', models.CharField(db_column='formula_id', max_length=20, primary_key=True, serialize=False, verbose_name='公式編號')),
                ('formula_name', models.CharField(db_column='formula_name', max_length=50, unique=True, verbose_name='公式名稱')),
                ('formula_rule', models.CharField(db_column='formula_rule', max_length=150, verbose_name='公式規則')),
                ('formula_unit', models.CharField(choices=[('0', '其它'), ('1', '日期'), ('2', '天'), ('3', '次'), ('4', '元'), ('5', '百分比')], db_column='formula_unit', max_length=3, verbose_name='公式單位')),
                ('descr', models.CharField(db_column='descr', max_length=200, verbose_name='公式說明')),
                ('cuser', models.CharField(db_column='cuser', max_length=20, verbose_name='創始人')),
                ('cdate', models.DateField(auto_now_add=True, db_column='cdate', verbose_name='創立日期')),
                ('ctime', models.TimeField(auto_now_add=True, db_column='ctime', verbose_name='創立時間')),
                ('muser', models.CharField(db_column='muser', max_length=20, verbose_name='異動者')),
                ('mdate', models.DateField(auto_now=True, db_column='mdate', verbose_name='異動日期')),
                ('mtime', models.TimeField(auto_now=True, db_column='mtime', verbose_name='異動時間')),
                ('cpnyid', models.ForeignKey(db_column='cpnyid', on_delete=django.db.models.deletion.CASCADE, to='basic_data.crm_company', verbose_name='公司品牌')),
            ],
            options={
                'db_table': 'Formula',
            },
        ),
    ]
