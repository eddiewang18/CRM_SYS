from django.db import models

# Create your models here.

class CRM_COMPANY(models.Model):
    cpnyid = models.CharField(primary_key=True,max_length=10,db_column="cpnyid",verbose_name="公司別")
    cocname = models.CharField(max_length=255,db_column="cocname",verbose_name='公司中文名稱')
    coename = models.CharField(max_length=255,db_column="coename",verbose_name='公司英文名稱',blank=True,null=True)    
    coscname = models.CharField(max_length=255,db_column="coscname",verbose_name='公司中文簡稱',blank=True,null=True)
    cosename = models.CharField(max_length=255,db_column="cosename",verbose_name='公司英文簡稱',blank=True,null=True) 
    cuser = models.CharField(max_length=20,db_column="cuser",verbose_name='創始人') 
    cdate = models.DateField(db_column="cdate",verbose_name='創立日期',auto_now_add=True)
    ctime = models.TimeField(db_column="ctime",verbose_name='創立時間',auto_now_add=True)
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)

    class Meta:
        db_table = "CRM_COMPANY"    