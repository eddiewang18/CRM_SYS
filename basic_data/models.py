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
        print(f"----------\n開始查詢數據")
        print(f'queryDict:{queryDict}')
        for queryType, fields in self.fieldQueryRule.items():
            # 依不同欄位的類型queryType(有的欄位用equal查詢 有的欄位用like....)
            # 如果查詢類型有對應的欄位則進行資料查詢 篩選
            if len(fields)>0 :
                for field in fields:
                    qdict = {}
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
                    if count1==0:
                        qs_result = qs_result.objects.filter(**qdict)
                        count1+=1
                    else :
                        qs_result = qs_result.filter(**qdict)
                    print(f'queryType:{queryType}')
                    print(f'qdict:{qdict}')
                    print(f'qs_result:{qs_result}')
                    print("\n")
        #     else:
        #         count+=1
        # if count%len(self.fieldQueryRule)==0:
        #     return self.__class__.objects.all()
        print(f"結束查詢數據\n----------")
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


