from django.db import models
import datetime
from basic_data.models import(
    CrmQueryData,
    CRM_COMPANY,
    SHOP,
    VIPINFO,
    Product
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
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)
    class Meta:
        db_table = "Paramater"  

class Formula(models.Model):
    formula_id = models.CharField(primary_key=True,max_length=25,db_column="formula_id",verbose_name='公式編號') 
    formula_name = models.CharField(max_length=50,db_column="formula_name",verbose_name='公式名稱',unique=True) 
    formula_rule = models.CharField(max_length=150,db_column="formula_rule",verbose_name='公式規則') 
    formula_note = models.CharField(max_length=150,db_column="formula_note",verbose_name='公式中文規則',null=True) 
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
    label_gname = models.CharField(max_length=50,db_column='label_gname',verbose_name='標籤群組名稱')
    formula_id = models.ForeignKey(to="Formula",to_field='formula_id',db_column="formula_id",verbose_name='標籤計算公式',on_delete=models.CASCADE) 
    descr = models.TextField(db_column="descr",verbose_name="標籤群組描述",blank=True,null=True)
    color = models.CharField(db_column='color',verbose_name='標籤群組標記顏色',max_length=8)
    xor_choices = [('0','允許選擇多標籤'),('1','僅能選擇單一標籤')]
    xor = models.CharField(db_column="isxor",verbose_name='貼標時客人是否可以擁有群組內一個以上的標籤',max_length=2,choices=xor_choices,default='1')
    label_enable_choices = [('0','否'),('1','是')]
    label_enable = models.CharField(db_column="label_enable",verbose_name='是否停用',max_length=2,choices=label_enable_choices,default='0')
    cuser = models.CharField(max_length=20,db_column="cuser",verbose_name='創始人',default='admin') 
    cdate = models.DateField(db_column="cdate",verbose_name='創立日期',auto_now_add=True)
    ctime = models.TimeField(db_column="ctime",verbose_name='創立時間',auto_now_add=True)
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者',default='admin') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)
    sys_create = models.CharField(max_length=2,db_column='sys_create',verbose_name='系統預設創建標籤',null=True,blank=True)
    class Meta:
        db_table = "VIP_LABEL_GROUP"  
        unique_together = ('cpnyid', 'label_gname')

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
    label_name = models.CharField(max_length=50,db_column='label_name',verbose_name='標籤名稱')
    calmin = models.DecimalField(max_digits=10, decimal_places=2,db_column='calmin',verbose_name='計算區間起')
    calmax = models.DecimalField(max_digits=10, decimal_places=2,db_column='calmax',verbose_name='計算區間迄')
    label_enable_choices = [('0','否'),('1','是')]
    label_enable = models.CharField(db_column="label_enable",verbose_name='是否停用',max_length=2,choices=label_enable_choices,default='0')
    cuser = models.CharField(max_length=20,db_column="cuser",verbose_name='創始人',default='admin') 
    cdate = models.DateField(db_column="cdate",verbose_name='創立日期',auto_now_add=True)
    ctime = models.TimeField(db_column="ctime",verbose_name='創立時間',auto_now_add=True)
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者',default='admin') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)
    sys_create = models.CharField(max_length=2,db_column='sys_create',verbose_name='系統預設創建標籤',null=True,blank=True)    
    def __str__(self):
        return  self.label_name   

    class Meta:
        db_table = "VIP_LABEL"  
        unique_together = ('label_gid', 'label_name')

class Sales00(models.Model):
    sale00_id = models.CharField(primary_key=True,max_length=30,db_column="sale00_id",verbose_name='銷售單據單號') 
    cpnyid  = models.ForeignKey(to="basic_data.CRM_COMPANY",to_field='cpnyid',db_column='cpnyid',verbose_name='公司品牌',on_delete=models.CASCADE)
    shop_id = models.ForeignKey(to="basic_data.SHOP",to_field="shop_id",on_delete=models.CASCADE,db_column='shop_id',verbose_name='消費分店')
    vip_id = models.ForeignKey(to="basic_data.VIPINFO",to_field="vip_id",on_delete=models.CASCADE,db_column='vip_id',verbose_name='會員編號')
    input_date = models.DateField(db_column='input_date',verbose_name='入賬(消費)日期',default=datetime.datetime.now().date())
    card_no = models.CharField(max_length=30,db_column="card_no",verbose_name='會員卡號',blank=True,null=True) 
    sale_status_choices = [('1','存檔'),('2','作廢')]
    sale_status = models.CharField(max_length=2,db_column="sale_status",verbose_name='交易狀態',blank=True,null=True,default='1',choices=sale_status_choices)
    sale_type_choices = [('1','普通'),('2','訂貨提領'),('3','有換貨')]
    sale_type = models.CharField(max_length=2,db_column="sale_type",verbose_name='銷售類型',blank=True,null=True,default='1',choices=sale_type_choices)
    goods_type_choices = [('1','銷貨單'),('2','銷退單'),('3','已被退銷貨單')]
    goods_type =  models.CharField(max_length=2,db_column="goods_type",verbose_name='退貨標誌',blank=True,null=True,default='1',choices=goods_type_choices)
    tot_quan =  models.IntegerField(db_column="tot_quan",verbose_name='總銷售數量') 
    tot_sales = models.IntegerField(db_column="tot_sales",verbose_name='總銷售金額') 
    cuser = models.CharField(max_length=20,db_column="cuser",verbose_name='創始人') 
    cdate = models.DateField(db_column="cdate",verbose_name='創立日期',auto_now_add=True)
    ctime = models.TimeField(db_column="ctime",verbose_name='創立時間',auto_now_add=True)
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)

    class Meta:
        db_table = "sales00"  
        unique_together = ('cpnyid', 'shop_id', 'sale00_id')



class Sale01(models.Model):
    sale01_id = models.CharField(primary_key=True,max_length=30,db_column="sale01_id") 
    sales_sno = models.CharField(max_length=30,db_column="sales_sno",verbose_name='交易明細序號') 
    sale00_id = models.ForeignKey(to="Sales00",to_field='sale00_id',db_column='sale00_id',verbose_name='銷售單據單號',on_delete=models.CASCADE)
    cpnyid  = models.ForeignKey(to="basic_data.CRM_COMPANY",to_field='cpnyid',db_column='cpnyid',verbose_name='公司品牌',on_delete=models.CASCADE)
    shop_id = models.ForeignKey(to="basic_data.SHOP",to_field="shop_id",on_delete=models.CASCADE,db_column='shop_id',verbose_name='消費分店')
    prod_id = models.ForeignKey(to="basic_data.Product",to_field="prod_id",on_delete=models.CASCADE,db_column='prod_id',verbose_name='商品編號')
    qty = models.IntegerField(db_column="qty",verbose_name='購買商品數量') 
    price =  models.IntegerField(db_column="price",verbose_name='商品單價') 

    class Meta:
        db_table = "sales01"  
        unique_together = ('sale00_id', 'sales_sno', 'prod_id')




class PARAMATER_STAT(models.Model):
    cpnyid  = models.ForeignKey(to="basic_data.CRM_COMPANY",to_field='cpnyid',db_column='cpnyid',verbose_name='公司品牌',on_delete=models.CASCADE)
    vip_id = models.ForeignKey(to="basic_data.VIPINFO",to_field="vip_id",on_delete=models.CASCADE,db_column='vip_id',verbose_name='會員編號')
    param_id = models.ForeignKey(to="Paramater",to_field="param_id",on_delete=models.CASCADE,db_column='param_id',verbose_name='參數編號')
    param_value =  models.CharField(max_length=30,db_column="param_value",verbose_name='參數值')
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)     
    class Meta:
        db_table = "paramater_stat"  
        unique_together = ('cpnyid', 'vip_id', 'param_id')

class PARAMATER_STAT_COMPANY(models.Model):
    cpnyid  = models.ForeignKey(to="basic_data.CRM_COMPANY",to_field='cpnyid',db_column='cpnyid',verbose_name='公司品牌',on_delete=models.CASCADE)
    param_id = models.ForeignKey(to="Paramater",to_field="param_id",on_delete=models.CASCADE,db_column='param_id',verbose_name='參數編號')
    param_value =  models.CharField(max_length=30,db_column="param_value",verbose_name='參數值')
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)     
    
    class Meta:
        db_table = "paramater_stat_company"  
        unique_together = ('cpnyid', 'param_id')



class VIP_FORMULA_STAT(models.Model):
    cpnyid  = models.ForeignKey(to="basic_data.CRM_COMPANY",to_field='cpnyid',db_column='cpnyid',verbose_name='公司品牌',on_delete=models.CASCADE)
    vip_id = models.ForeignKey(to="basic_data.VIPINFO",to_field="vip_id",on_delete=models.CASCADE,db_column='vip_id',verbose_name='會員編號')
    formula_id = models.ForeignKey(to="Formula",to_field="formula_id",on_delete=models.CASCADE,db_column='formula_id',verbose_name='公式編號') 
    result_value =   models.CharField(max_length=30,db_column="result_value",verbose_name='計算結果值')
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)     
    
    class Meta:
        db_table = "vip_formula_stat"  
        unique_together = ('cpnyid','vip_id', 'formula_id')       

class VIP_LABEL_STAT(models.Model):
    cpnyid  = models.ForeignKey(to="basic_data.CRM_COMPANY",to_field='cpnyid',db_column='cpnyid',verbose_name='公司品牌',on_delete=models.CASCADE)
    vip_id = models.ForeignKey(to="basic_data.VIPINFO",to_field="vip_id",on_delete=models.CASCADE,db_column='vip_id',verbose_name='會員編號')  
    label_id = models.ForeignKey(to="VIP_LABEL",to_field='label_id',db_column='label_id',verbose_name='標籤編號',on_delete=models.CASCADE)
    calsdate = models.DateField(blank=True,null=True,verbose_name='計算日起',db_column='calsdate')
    caledate = models.DateField(blank=True,null=True,verbose_name='計算日迄',db_column='caledate')
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)     
    
    class Meta:
        db_table = "vip_label_stat"  
        unique_together = ('cpnyid','vip_id', 'label_id')     