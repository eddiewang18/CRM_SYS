from django.db import models

# Create your models here.


class CrmQueryData():

    #此系統查詢資料的主要4種方式>欄位 = 值  , 欄位 like %值%  , 欄位 < 上限值 and 欄位 > 下限值  , 欄位 between 起始日 and 截止日
    fieldQueryRule = {
	"equals":[],
	"like":[],
	'date_range':[],
	'number_range':[],
    }

    def crmQdata(self,queryDict):
        qs_result = self.__class__
        count = 0 # 用來輔助判斷最後查詢的結果是否為全查
        count1 = 0
        # print(f"----------\n開始查詢數據")
        # print(f'queryDict:{queryDict}')
        for queryType, fields in self.fieldQueryRule.items():
            # 依不同欄位的類型queryType(有的欄位用equal查詢 有的欄位用like....)
            # 如果查詢類型有對應的欄位則進行資料查詢 篩選
            if len(fields)>0 :
                for field in fields:
                    qdict = {}
                    try:
                        if queryType=='equal':
                            queryValue = queryDict.get(field)
                            if len(queryValue)>0:
                                qdict[field]=queryValue
                            
                        if queryType=='like':
                            queryValue = queryDict.get(field)
                            if len(queryValue)>0:
                                qdict[field+'__icontains']=queryValue
                        if queryType=='date_range':
                            sdate = queryDict.get(field+"_sdate")
                            edate = queryDict.get(field+"_edate")
                            if len(queryValue)>0:
                                qdict[field+'__range']=[sdate,edate]
                        if queryType=='number_range':
                            upperVal = queryDict.get(field+"_upperVal")
                            lowerVal = queryDict.get(field+"_lowerVal")
                            if len(upperVal)>0 or len(lowerVal)>0:
                                qdict[field+'__range']=[lowerVal,upperVal]
                    except:
                        continue
                    if count1==0:
                        qs_result = qs_result.objects.filter(**qdict)
                        count1+=1
                    else :
                        qs_result = qs_result.filter(**qdict)
                    # print(f'queryType:{queryType}')
                    # print(f'qdict:{qdict}')
                    # print(f'qs_result:{qs_result}')
                    # print("\n")

        # print(f"結束查詢數據\n----------")
        return qs_result



class CRM_COMPANY(models.Model,CrmQueryData):
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

    fieldQueryRule = {
        "equals":[],
        "like":['cpnyid',"cocname","coename","cosename"],
        'date_range':[],
        'number_range':[],
        }  
    def __str__(self):
        return self.cocname

class SHOPGROUP(models.Model,CrmQueryData):
    shopgroup_id = models.CharField(primary_key=True,max_length=10,db_column="shopgroup_id",verbose_name="群組編號")
    shopgroup_name = models.CharField(max_length=50,db_column="shopgroup_name",verbose_name="群組名稱",unique=True)
    cuser = models.CharField(max_length=20,db_column="cuser",verbose_name='創始人') 
    cdate = models.DateField(db_column="cdate",verbose_name='創立日期',auto_now_add=True)
    ctime = models.TimeField(db_column="ctime",verbose_name='創立時間',auto_now_add=True)
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)

    def __str__(self):
        return  self.shopgroup_name   

    class Meta:
        db_table = "SHOPGROUP"  

    fieldQueryRule = {
        "equals":[],
        "like":['shopgroup_id',"shopgroup_name"],
        'date_range':[],
        'number_range':[],
        }  


class County(models.Model):
    county_id = models.CharField(primary_key=True,max_length=10,db_column='county_id',verbose_name='縣市代號')
    county_name = models.CharField(max_length=60,db_column='county_name',verbose_name='縣市名稱',unique=True)
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者',default='admin') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)

    def __str__(self):
        return self.county_name

    class Meta:
        db_table = "County"  

class Area(models.Model):
    county_id = models.ForeignKey(to='County',to_field='county_id',verbose_name='所屬縣市',db_column="county_id",on_delete=models.CASCADE)
    post_id = models.CharField(primary_key=True,max_length=10,db_column='post_id',verbose_name='地區代號')
    post_name = models.CharField(max_length=60,db_column='post_name',verbose_name='地區名稱')
    postal = models.CharField(max_length=10,db_column='postal',verbose_name='郵遞區號')
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者',default='admin') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)
    def __str__(self):
        return self.post_name

    class Meta:
        db_table = "Area"  


class SHOP(models.Model,CrmQueryData):
    cpnyid               = models.ForeignKey(to="CRM_COMPANY",to_field='cpnyid',db_column='cpnyid',verbose_name='公司品牌',on_delete=models.CASCADE)
    shop_id              = models.CharField(primary_key=True,max_length=10,db_column='shop_id',verbose_name='分店編號')
    shop_name            = models.CharField(max_length=30,db_column='shop_name',verbose_name='分店名稱',unique=True)
    shop_scname          = models.CharField(blank=True,null=True,max_length=10,db_column='shop_scname',verbose_name='分店簡稱')
    shop_kind_choices = [("0","總店"),("1","直營店"),("2","加盟店")]
    shop_kind            = models.CharField(blank=True,null=True,max_length=10,db_column='shop_kind',verbose_name='分店類型',choices=shop_kind_choices)
    shopgroup_id         = models.ForeignKey(blank=True,null=True,to='SHOPGROUP',to_field='shopgroup_id',db_column="shopgroup_id",verbose_name="分店群組",on_delete=models.CASCADE)
    shop_chief           = models.CharField(blank=True,null=True,max_length=50,db_column='shop_chief',verbose_name='分店店長')
    shop_disable_choices = [('0','停業'),('1','營業中')]
    shop_disable         = models.CharField(blank=True,null=True,max_length=1,db_column='shop_disable',verbose_name='營業狀態',choices=shop_disable_choices,default='1')
    shop_disable_date    = models.DateField(blank=True,null=True,db_column='shop_disable_date',verbose_name='停業日期')
    shop_note            = models.CharField(blank=True,null=True,max_length=50,db_column='shop_note',verbose_name='分店說明')
    county_id            = models.ForeignKey(blank=True,null=True,to='County',to_field='county_id',verbose_name='所在縣市',db_column="county_id",on_delete=models.CASCADE)
    post_id              = models.ForeignKey(blank=True,null=True,to='Area',to_field='post_id',verbose_name='所在地區',db_column="post_id",on_delete=models.CASCADE)
    fax                  = models.CharField(blank=True,null=True,max_length=30,db_column='fax',verbose_name='傳真號碼')
    telno                =  models.CharField(blank=True,null=True,max_length=20,db_column='telno',verbose_name='電話號碼')
    cuser                = models.CharField(max_length=20,db_column="cuser",verbose_name='創始人') 
    cdate                = models.DateField(db_column="cdate",verbose_name='創立日期',auto_now_add=True)
    ctime                = models.TimeField(db_column="ctime",verbose_name='創立時間',auto_now_add=True)
    muser                = models.CharField(max_length=20,db_column="muser",verbose_name='異動者') 
    mdate                = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime                = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)

    def __str__(self):
        return self.shop_name

    class Meta:
        db_table = "SHOP"  
    
    fieldQueryRule = {
        "equals":['shop_kind','shopgroup_id',"shop_disable","county_id","post_id"],
        "like":['cpnyid',"shop_id","shop_name","shop_scname","shop_chief","shop_note","fax","telno"],
        'date_range':["shop_disable_sdate","shop_disable_edate"],
        'number_range':[],
        }  