from django.db import models
from django.utils import timezone
# Create your models here.


class CrmQueryData():

    #此系統查詢資料的主要4種方式>欄位 = 值  , 欄位 like %值%  , 欄位 < 上限值 and 欄位 > 下限值  , 欄位 between 起始日 and 截止日
    fieldQueryRule = {
	"equals":[],
	"like":[],
	'date_range':[],
	'number_range':[],
    }

    def crmQdata(self,queryDict,fk_list={}):
        qs_result = self.__class__
        count = 0 # 用來輔助判斷最後查詢的結果是否為全查
        count1 = 0
        print("================查詢數據開始=====================")
        print(f'查詢條件(queryDict):{queryDict}\n')
        for queryType, fields in self.fieldQueryRule.items():
            # 依不同欄位的類型queryType(有的欄位用equal查詢 有的欄位用like....)
            # 如果查詢類型有對應的欄位則進行資料查詢 篩選
            print("----------------------")
            print(f"查詢類型 {queryType} 開始:")
            if len(fields)>0 :
                for field in fields:
                    print("#####################")
                    print(f"查詢欄位:{field}")
                    qdict = {}
                    try:
                        if queryType=='equals':
                            queryValue = queryDict.get(field)
                            print(f'queryValue:{queryValue}')
                            if len(queryValue)>0:
                                if field in fk_list:
                                    field = fk_list[field]
                                qdict[field]=queryValue

                        if queryType=='like':
                            queryValue = queryDict.get(field)
                            print(f'queryValue:{queryValue}')
                            if len(queryValue)>0:
                                if field in fk_list:
                                    field = fk_list[field]
                                qdict[field+'__icontains']=queryValue
                        if queryType=='date_range':
                            sdate = queryDict.get(field+"_sdate")
                            edate = queryDict.get(field+"_edate")
                            if len(sdate)>0 or len(edate)>0:
                                if field in fk_list:
                                    field = fk_list[field]
                                qdict[field+'__range']=[sdate,edate]
                        if queryType=='number_range':
                            upperVal = queryDict.get(field+"_upperVal")
                            lowerVal = queryDict.get(field+"_lowerVal")
                            if len(upperVal)>0 or len(lowerVal)>0:
                                if field in fk_list:
                                    field = fk_list[field]
                                qdict[field+'__range']=[lowerVal,upperVal]
                    except Exception as err:
                        print(f'查詢時的例外訊息:{str(err)}')
                        continue
                    print(f"下的查詢條件:{qdict}")
                    if count1==0:
                        qs_result = qs_result.objects.filter(**qdict)
                        count1+=1
                    else :
                        qs_result = qs_result.filter(**qdict)
                    print(f"依條件查詢的返回結果:{qs_result}")
                    # print(f'queryType:{queryType}')
                    # print(f'qdict:{qdict}')
                    # print(f'qs_result:{qs_result}')
                    print("#####################")

            print(f"查詢類型 {queryType} 結束!")                
        print(f"最終的查詢結果:\n{qs_result}")
        print("================查詢數據結束=====================")
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
    fk_list = {
    }


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
    fk_list = {
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
        'date_range':["shop_disable_date"],
        'number_range':[],
        }  
    # fk_list 紀錄該model中對應的外鍵欄位
    fk_list = {
        'cpnyid':'cpnyid__cpnyid',
        'shopgroup_id':"shopgroup_id__shopgroup_id",
        'county_id':"county_id__county_id",
        "post_id":"post_id__post_id"
    }



class HRUSER_GROUP(models.Model):
    group_id   = models.CharField(primary_key=True,max_length=10,db_column='group_id',verbose_name="員工群組編號")
    group_name = models.CharField(max_length=20,db_column="group_name",verbose_name="員工群組名稱")
    cuser = models.CharField(max_length=20,db_column="cuser",verbose_name='創始人') 
    cdate = models.DateField(db_column="cdate",verbose_name='創立日期',auto_now_add=True)
    ctime = models.TimeField(db_column="ctime",verbose_name='創立時間',auto_now_add=True)
    muser = models.CharField(max_length=20,db_column="muser",verbose_name='異動者') 
    mdate = models.DateField(db_column="mdate",verbose_name='異動日期',auto_now=True)
    mtime = models.TimeField(db_column="mtime",verbose_name='異動時間',auto_now=True)

    def __str__(self):
        return  self.group_name   

    class Meta:
        db_table = "HRUSER_GROUP"
  

    fieldQueryRule = {
        "equals":[],
        "like":['group_id',"group_name"],
        'date_range':[],
        'number_range':[],
        }  
    fk_list = {
    }


class CRM_HRUSER(models.Model,CrmQueryData):
    cpnyid = models.ForeignKey(to="CRM_COMPANY",to_field='cpnyid',db_column='cpnyid',verbose_name='所屬公司品牌',on_delete=models.CASCADE)
    empid = models.CharField(primary_key=True,max_length=20,db_column="empid",verbose_name='員工編號')
    cname = models.CharField(max_length=20,db_column="cname",verbose_name="姓名")
    ename = models.CharField(max_length=50,db_column="ename",verbose_name="英文姓名",blank=True,null=True)
    identid =  models.CharField(max_length=20,db_column="identid",verbose_name="身份證號",blank=True,null=True)
    birthday = models.DateField(db_column="birthday",verbose_name="出生日期",blank=True,null=True)
    pwd = models.CharField(max_length=20,db_column="pwd",verbose_name="密碼")
    telno  = models.CharField(max_length=20,db_column="telno",verbose_name="聯絡電話",blank=True,null=True)
    mobilno  = models.CharField(max_length=20,db_column="mobilno",verbose_name="行動電話",blank=True,null=True)
    sex_choices = [("0","女"),("1","男")]
    sex = models.CharField(max_length=2,db_column="sex",verbose_name="性別",blank=True,null=True,choices=sex_choices)
    email = models.CharField(max_length=255,db_column="email",verbose_name="電子信箱",blank=True,null=True)
    indate = models.DateField(db_column="indate",verbose_name="到職日期",blank=True,null=True)
    quitdate = models.DateField(db_column="quitdate",verbose_name="離職日期",blank=True,null=True)
    group_id   = models.ForeignKey(to="HRUSER_GROUP",to_field='group_id',db_column='group_id',verbose_name='所屬員工群組',on_delete=models.CASCADE,blank=True,null=True)
    shop_id   = models.ForeignKey(to="SHOP",to_field='shop_id',db_column='shop_id',verbose_name='歸屬分店',on_delete=models.CASCADE)
    emp_type_choices = [("0","系統管理者"),("1","總部使用者"),("2","分店店長"),("3","分店員工")]
    emp_type = models.CharField(max_length=2,db_column="emp_type",verbose_name="員工類型",blank=True,null=True,choices=emp_type_choices,default="3")
    county_id  = models.ForeignKey(blank=True,null=True,to='County',to_field='county_id',verbose_name='所在縣市',db_column="county_id",on_delete=models.CASCADE)
    post_id    = models.ForeignKey(blank=True,null=True,to='Area',to_field='post_id',verbose_name='所在地區',db_column="post_id",on_delete=models.CASCADE)
    note = models.TextField(max_length=255,db_column='note',verbose_name="備註",blank=True,null=True)

    def __str__(self):
        return f"{self.empid} {self.cname}"

    class Meta:
        db_table = "CRM_HRUSER"  
    
    fieldQueryRule = {
        "equals":['pwd','cpnyid',"group_id","shop_id","sex","emp_type","county_id","post_id"],
        "like":["empid","cname","ename","identid","telno","mobilno",'email',"note"],
        'date_range':["birthday","indate",'quitdate'],
        'number_range':[],
        }  
    # fk_list 紀錄該model中對應的外鍵欄位
    fk_list = {
        'cpnyid':'cpnyid__cpnyid',
         'shop_id':"shop_id__shop_id",
        'group_id':"group_id__group_id",
        'county_id':"county_id__county_id",
        "post_id":"post_id__post_id"
    }