from django.db import models
from basic_data.models import(
    CrmQueryData
 
) 
# Create your models here.
class Paramater(models.Model):
    param_id = models.CharField(primary_key=True,max_length=50,db_column="param_id",verbose_name='參數編號') 
    param_name = models.CharField(max_length=50,db_column="param_name",verbose_name='參數名稱',unique=True) 
    unit_choices = [('0','其它'),('1',"日期"),("2","天"),("3","次"),("4","元"),("5","百分比")]
    param_unit = models.CharField(max_length=3,db_column="param_unit",verbose_name='參數單位',choices=unit_choices) 
    descr = models.CharField(max_length=200,db_column="descr",verbose_name='公式說明') 
    is_brand_choices = [("Y","是"),("N","否")]
    is_brand = models.CharField(max_length=2,db_column="is_brand",verbose_name='判斷是否為品牌變數',choices=is_brand_choices) 

    class Meta:
        db_table = "Paramater"  

class Formula(models.Model):
    formula_id = models.CharField(primary_key=True,max_length=25,db_column="formula_id",verbose_name='公式編號') 
    formula_name = models.CharField(max_length=50,db_column="formula_name",verbose_name='公式名稱',unique=True) 
    formula_rule = models.CharField(max_length=150,db_column="formula_rule",verbose_name='公式規則') 
    unit_choices = [('0','其它'),('1',"日期"),("2","天"),("3","次"),("4","元"),("5","百分比")]
    formula_unit = models.CharField(max_length=3,db_column="formula_unit",verbose_name='公式單位',choices=unit_choices) 
    descr = models.CharField(max_length=200,db_column="descr",verbose_name='公式說明') 
    cuser = models.CharField(max_length=20,db_column="cuser",verbose_name='創始人') 
    cdate = models.DateField(db_column="cdate",verbose_name='創立日期',auto_now_add=True)
    ctime = models.TimeField(db_column="ctime",verbose_name='創立時間',auto_now_add=True)
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)
    def __str__(self):
        return  self.formula_name   

    class Meta:
        db_table = "Formula"  

    fieldQueryRule = {
        "equals":["cpnyid","formula_unit"],
        "like":['formula_id',"formula_name","formula_rule"],
        'date_range':[],
        'number_range':[],
        }  
    fk_list = {
        'cpnyid':'cpnyid__cpnyid',
    }    


class VIP_LABEL_GROUP(models.Model,CrmQueryData):
    cpnyid = models.ForeignKey(to="basic_data.CRM_COMPANY",to_field='cpnyid',db_column='cpnyid',verbose_name='公司品牌',on_delete=models.CASCADE)
    label_gid = models.CharField(max_length=20,primary_key=True,db_column='label_gid',verbose_name="標籤群組代號")
    label_gname = models.CharField(max_length=50,db_column='label_gname',verbose_name='標籤群組名稱',unique=True)
    formula_id = models.ForeignKey(to="Formula",to_field='formula_id',db_column="formula_id",verbose_name='標籤計算公式',on_delete=models.CASCADE) 
    descr = models.TextField(db_column="descr",verbose_name="標籤群組描述",blank=True,null=True)
    color = models.CharField(db_column='color',verbose_name='標籤群組標記顏色',max_length=8)
    xor_choices = [('0','允許選擇多標籤'),('1','僅能選擇單一標籤')]
    xor = models.CharField(db_column="xor",verbose_name='貼標時客人是否可以擁有群組內一個以上的標籤',max_length=2,choices=xor_choices,default='1')
    label_enable_choices = [('0','否'),('1','是')]
    label_enable = models.CharField(db_column="label_enable",verbose_name='是否停用',max_length=2,choices=label_enable_choices,default='0')
    cuser = models.CharField(max_length=20,db_column="cuser",verbose_name='創始人') 
    cdate = models.DateField(db_column="cdate",verbose_name='創立日期',auto_now_add=True)
    ctime = models.TimeField(db_column="ctime",verbose_name='創立時間',auto_now_add=True)
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)

    class Meta:
        db_table = "VIP_LABEL_GROUP"  

    fieldQueryRule = {
        "equals":["cpnyid","xor","label_enable","formula_id"],
        "like":['label_gid',"label_gname","descr"],
        'date_range':[],
        'number_range':[],
        }  
    fk_list = {
        'cpnyid':'cpnyid__cpnyid',
        'formula_id':"formula_id__formula_id"
    }    

class VIP_LABEL(models.Model):
    label_gid = models.ForeignKey(to="VIP_LABEL_GROUP",to_field='label_gid',db_column='label_gid',verbose_name="標籤群組代號",on_delete=models.CASCADE)
    label_id = models.CharField(primary_key=True,db_column="label_id",verbose_name="標籤代號",max_length=50)
    label_name = models.CharField(max_length=50,db_column='label_name',verbose_name='標籤名稱',unique=True)
    calmin = models.DecimalField(max_digits=10, decimal_places=2,db_column='calmin',verbose_name='計算區間起')
    calmax = models.DecimalField(max_digits=10, decimal_places=2,db_column='calmax',verbose_name='計算區間迄')
    label_enable_choices = [('0','否'),('1','是')]
    label_enable = models.CharField(db_column="label_enable",verbose_name='是否停用',max_length=2,choices=label_enable_choices,default='0')
    cuser = models.CharField(max_length=20,db_column="cuser",verbose_name='創始人') 
    cdate = models.DateField(db_column="cdate",verbose_name='創立日期',auto_now_add=True)
    ctime = models.TimeField(db_column="ctime",verbose_name='創立時間',auto_now_add=True)
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)

    def __str__(self):
        return  self.label_name   

    class Meta:
        db_table = "VIP_LABEL"  