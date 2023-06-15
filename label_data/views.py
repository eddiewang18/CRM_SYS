from django.shortcuts import render
from basic_data.views import (
    dataCuser,
    FnView
)
from basic_data.models import (
    CRM_COMPANY
)
from django.views import View
from .models import (
    VIP_LABEL_GROUP,
    VIP_LABEL,
    VIP_LABEL_STAT,
    Sales00,
    Formula
)
from .forms import (
    VIP_LABEL_GROUP_ModelForm,
    VIP_LABEL_GROUP_QModelForm,
    VIP_LABEL_ModelForm,
    VIP_LABEL_STATModelForm,
    VIP_LABEL_STATModelForm2
)
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import JsonResponse
import json
from pymysql import *
import datetime
import numpy as np
from datetime import date
# Create your views here.
class FnTableView(View):
    """
    屬性:
        model :  開發功能對應的 Model(主表)
        sub_model : 副表對應的model
        main_pk:主表在DB中的pk鍵
        sub_pk:副表在DB中的pk鍵
        model_form : 開發功能對應的 ModelForm
        table_form: 副表相關的modelform
        query_model_form : 開發功能按查尋按鈕時跳出來對應的查詢表單欄位
        result_model_form  : 開發功能結果顯示時跳出來對應的表單欄位
        html_file :  開發功能對應的html頁面
        return_query_cols : 查詢時要返回的欄位資料，以list的類別儲存 e.g. [col1,col2,.....]
        sub_table_show_cols : 在畫面中，副表顯示的欄位，以list 儲存

    """
    def get(self,request,defaultLab=None):
        if "get_subtable_data" in request.GET:
            main_table_pkfield_val = request.GET.get("main_table_pkfield_val")
            print(f"傳送過來的pk鍵:{main_table_pkfield_val}")
            sub_table_objs = list(self.sub_model.objects.filter(**{self.form_table_associate_key:main_table_pkfield_val}).values(*self.sub_table_show_cols))
            print(f'\n對應的副表資料{sub_table_objs}\n')
            return JsonResponse(sub_table_objs,safe=False)
        """
        get 方法返回ModelForm空白欄位表單
        """
        form = self.model_form()
        table_form = self.table_form()
        context = {
            'form':form,
            'table_form':table_form
        }

        if defaultLab:
            context['success']='成功匯入系統預設標籤'

        return render(request,self.html_file,context)

    
    def post(self,request):
        """
            post 方法:
                建立新的數據 : 當'create'存在於request.POST中，則會進行新增數據的動作
                查詢數據 : 當 'query' 存在於request.POST中，則會返回一個ModelForm空白欄位表單，作為使用者查詢資料的條件
                返回查詢條件的數據 : 當 'query' 存在於request.POST中，則會返回使用者依條件搜尋後的數據並以JSON的格式返回給前端
                刪除數據 : 當 'delete' 存在於request.POST中，則會刪除指定的數據
        """
        print(f'request.POST:{request.POST}')
        if 'create' in request.POST:
            request_data = json.loads(request.POST['requestData'])
            insertFormData = request_data['insertFormData']
            tableData = request_data['tableData']
            # print( request_data,type(request_data))
            # print(insertFormData,type(insertFormData))
            # print(tableData,type(tableData))
            form = self.model_form(data=insertFormData)
            context = {
                'form':form
            }
            if form.is_valid():
                table_data = form.save(commit=False)
                table_data.muser = request.user.username
                table_data.save()
                context['success']="成功儲存"  
                context['form']=self.model_form()
            else : 
                errMsg = ''
                if len(form.errList)>0:
                    errMsg=form.errList[0]
                return JsonResponse({"insert":"fail","errMsg":errMsg})

            insert_data = tableData.get("insert") # [{'shopgroup_id': 'wdf', 'shopgroup_name': '123'}, {'shopgroup_id': 'ewq', 'shopgroup_name': '234'}]

            print(f'\ninsert_data : {insert_data}\n')

            if len(insert_data)>0:
                for data_row in insert_data:
                    table_form = self.table_form(data=data_row)
                    print(f"table_form data {table_form.data}")
                    if table_form.is_valid():
                        table_data = table_form.save(commit=False)
                        table_data.muser = request.user.username
                        table_data.save()
                        print(f'\ncreate a new row\n')
                    else:
                        print(f'invalid reason : {table_form.errors}')
                        return JsonResponse({"insert":"fail","errMsg":table_form.errList[0]})


            return JsonResponse({"insert":"ok"})
        elif 'query' in request.POST:
            form = self.model_form()
            qform = self.query_model_form() 
            rform = self.verbose_name_fields
            # print(f'rform : {rform}\n')
            context = {
                'form':form,
                "qform":qform,
                "rform":rform,
                'queryModal':True,

            }
        
            return render(request,self.html_file,context)
        elif 'defaultLab' in request.POST:
            from datetime import datetime
            print(f"defaultLab 傳送post請求....")
            cpnyid = request.POST.get("cpnyid")
            cpny_obj = CRM_COMPANY.objects.get(pk=cpnyid)
            mdate = date.today()
            loc_dt = datetime.today() 
            loc_dt_format = loc_dt.strftime("%Y/%m/%d %H:%M:%S")
            mtime = loc_dt_format[11:]
            v = list(VIP_LABEL_GROUP.objects.filter(cpnyid=cpnyid,sys_create='y'))
            for i in v:
                print(i)
                i1= i.vip_label_set.all()
                print(i1)
                for h in i1 :
                    h.delete()
                print("---------------") 
            
            VIP_LABEL_GROUP.objects.filter(cpnyid=cpnyid,sys_create='y').delete() #先刪除原系統預設標籤
            default_lab_grp = [
                {"cpnyid":cpny_obj,"label_gid":f'{cpnyid}00A','label_gname':'顧客身份','formula_id':Formula.objects.get(pk='D01'),'descr':'判斷會員在該商店(公司品牌)的身份','color':'#f5d6d6','xor':'1','label_enable':'0','sys_create':'y'},
                {"cpnyid":cpny_obj,"label_gid":f'{cpnyid}00B','label_gname':'顧客狀態','formula_id':Formula.objects.get(pk='D02'),'descr':'判斷會員近期購買狀態','color':'#7ce4d8','xor':'1','label_enable':'0','sys_create':'y'},
                {"cpnyid":cpny_obj,"label_gid":f'{cpnyid}00C','label_gname':'購物頻次','formula_id':Formula.objects.get(pk='D05'),'descr':'判斷個體會員總購物次數位於品牌全體會員的哪段級距','color':'#a3d3ff','xor':'1','label_enable':'0','sys_create':'y'},
                {"cpnyid":cpny_obj,"label_gid":f'{cpnyid}00D','label_gname':'入店資歷','formula_id':Formula.objects.get(pk='D03'),'descr':'判斷會員首次消費的時間位於品牌開店至今的哪段時期','color':'#ff75ed','xor':'1','label_enable':'0','sys_create':'y'},
                {"cpnyid":cpny_obj,"label_gid":f'{cpnyid}00E','label_gname':'購物金額','formula_id':Formula.objects.get(pk='D06'),'descr':'判斷個體會員總購物金額位於品牌全體會員的哪段級距','color':'#c7f93e','xor':'1','label_enable':'0','sys_create':'y'},
                {"cpnyid":cpny_obj,"label_gid":f'{cpnyid}00F','label_gname':'近期購物情境','formula_id':Formula.objects.get(pk='D04'),'descr':'判斷會員最近交易的狀況','color':'#f2dc50','xor':'1','label_enable':'0','sys_create':'y'},
                ]
            default_lab = {
                f'{cpnyid}00A':[
                    {"label_id":f"{cpnyid}00A001","label_name":"新進顧客","calmin":1.00,"calmax":1.00},
                    {"label_id":f"{cpnyid}00A002","label_name":"購買大於一次的顧客","calmin":1.00,"calmax":1.00}
                ],
                f'{cpnyid}00B':[
                    {"label_id":f"{cpnyid}00B001","label_name":"主力常客","calmin":0.01,"calmax":0.50},
                    {"label_id":f"{cpnyid}00B002","label_name":"常客","calmin":0.51,"calmax":1.50},
                    {"label_id":f"{cpnyid}00B003","label_name":"瞌睡客","calmin":1.51,"calmax":2.50},
                    {"label_id":f"{cpnyid}00B004","label_name":"半睡客","calmin":2.51,"calmax":4.00},
                    {"label_id":f"{cpnyid}00B005","label_name":"沉睡客","calmin":4.01,"calmax":999999.00},
                ],
                f'{cpnyid}00C':[
                    {"label_id":f"{cpnyid}00C001","label_name":"低頻買家","calmin":0.00,"calmax":0.33},
                    {"label_id":f"{cpnyid}00C002","label_name":"中頻買家","calmin":0.34,"calmax":0.66},
                    {"label_id":f"{cpnyid}00C003","label_name":"高頻買家","calmin":0.67,"calmax":1.00},
                ],
                f'{cpnyid}00D':[
                    {"label_id":f"{cpnyid}00D001","label_name":"入店資歷_早期","calmin":0.00,"calmax":0.33},
                    {"label_id":f"{cpnyid}00D002","label_name":"入店資歷_中期","calmin":0.34,"calmax":0.66},
                    {"label_id":f"{cpnyid}00D003","label_name":"入店資歷_後期","calmin":0.67,"calmax":1.00},
                ],
                f'{cpnyid}00E':[
                    {"label_id":f"{cpnyid}00E001","label_name":"低消費買家","calmin":0.00,"calmax":0.33},
                    {"label_id":f"{cpnyid}00E002","label_name":"中消費買家","calmin":0.34,"calmax":0.66},
                    {"label_id":f"{cpnyid}00E003","label_name":"高消費買家","calmin":0.67,"calmax":1.00},
                ],
                f'{cpnyid}00F':[
                    {"label_id":f"{cpnyid}00F001","label_name":"長期未購買家","calmin":0.00,"calmax":0.33},
                    {"label_id":f"{cpnyid}00F002","label_name":"中期未購買家","calmin":0.34,"calmax":0.66},
                    {"label_id":f"{cpnyid}00F003","label_name":"最近買家","calmin":0.67,"calmax":1.00},
                ]
            }
                    

            for lab_grp in default_lab_grp:
                lab_grp_data = VIP_LABEL_GROUP.objects.create(**lab_grp)
                lab_list = default_lab[lab_grp['label_gid']]
                for lab in lab_list :
                    lab['label_gid']=lab_grp_data
                    VIP_LABEL.objects.create(**lab)
            return self.get(request,defaultLab=True)

        elif 'update' in request.POST:
            request_data = json.loads(request.POST['requestData'])
            updateData = request_data['updateData']
            tableData = request_data['tableData']
            insert_data = tableData.get("insert") # [{'shopgroup_id': 'wdf', 'shopgroup_name': '123'}, {'shopgroup_id': 'ewq', 'shopgroup_name': '234'}]
            update_data = tableData.get("update")
            delete_data = tableData.get('delete')
            main_pk_val = updateData[self.main_pk]

            form_obj = self.model.objects.filter(pk=updateData[self.main_pk]).first()

            form = self.model_form(instance=form_obj,data=updateData)
            context = {
                'form':form
            }
            if form.is_valid():
                table_data = form.save(commit=False)
                table_data.muser = request.user.username
                table_data.save()
            else : 
                errMsg = ''
                if len(form.errList)>0:
                    errMsg=form.errList[0]
                return JsonResponse({"update":"fail","errMsg":errMsg})

            if len(delete_data)>0:
                for data_row in delete_data:
                    self.sub_model.objects.get(pk=data_row[self.sub_pk]).delete()
                    print(f'\ndelete a row\n')

            if len(insert_data)>0:
                for data_row in insert_data:
                    table_form = self.table_form(data=data_row)
                    print(f"table_form data {table_form.data}")
                    if table_form.is_valid():
                        table_data = table_form.save(commit=False)
                        table_data.muser = request.user.username
                        table_data.save()
                    else:
                        print(f'invalid reason : {table_form.errors}')
                        return JsonResponse({"update":"fail","errMsg":table_form.errList[0]})
            
            if len(update_data)>0:
                for data_row in update_data:
                    obj =self.sub_model.objects.filter(pk=data_row[self.sub_pk]).first()
                    form =  self.table_form(instance=obj,data=data_row)
                    if form.is_valid():
                        table_data = form.save(commit=False)
                        table_data.muser = request.user.username
                        table_data.save()
                    else:
                        print(f'invalid reason : {form.errors}')
                        return JsonResponse({"update":"fail","errMsg":form.errList[0]})


            return JsonResponse({"update":"ok"})
        elif 'delete' in request.POST:
            mainPkField_val = request.POST.get("mainPkField_val")
            obj = self.model.objects.filter(pk=mainPkField_val).first()
            obj.delete()
            return JsonResponse({})
        # 用axios發送post
        elif "querySubmit" in  json.loads(request.body.decode('utf-8'))['params']:
            requestData =json.loads(json.loads(request.body.decode('utf-8'))['params']['requestData'])
            print(f'\n查詢條件:{requestData}\n')
            result_query = list(self.model().crmQdata(requestData,self.model.fk_list).values(*self.return_query_cols ))
            print(f'\n查詢時回傳的資料:\n{result_query}|type:{type(result_query)}\n')
            return JsonResponse(result_query,safe=False)




        elif "delete" in  json.loads(request.body.decode('utf-8'))['params']:
            requestData =json.loads(request.body.decode('utf-8'))
            pk_fields = json.loads(requestData['params']['pk_fields']) 
            del_instance = self.model().crmQdata(pk_fields,self.model.fk_list)[0]
            del_instance.delete()
            return JsonResponse({})



class B01View(FnTableView):
    model = VIP_LABEL_GROUP
    model_form = VIP_LABEL_GROUP_ModelForm
    main_pk = "label_gid"
    table_form =  VIP_LABEL_ModelForm
    query_model_form = VIP_LABEL_GROUP_QModelForm
    verbose_name_fields = model_form().verbose_name_fields
    html_file = 'label_data/B01.html'
    return_query_cols = model_form().return_query_cols
    form_table_associate_key = 'label_gid'
    sub_model = VIP_LABEL
    sub_pk = "label_id"
    sub_table_show_cols = ["label_id","label_name","calmin","calmax","label_enable"]

dataCuser(VIP_LABEL_GROUP)

from pymysql import *

db_settings = {
"host":"127.0.0.1",
"port":3306,
"user":'root',
"password":'eddieWANG#183120880215',
'db':'crm01',
}


from django.core.paginator import Paginator, EmptyPage

class B02View(View):
    def get(self,request):
        form = VIP_LABEL_STATModelForm()
        return render(request,'label_data/B02.html',{'form':form})
    def post(self,request):
        print(f'b02傳送資料:{request.POST}')
        print()
        cpnyid = request.POST.get('cpnyid')
        print(f'cpnyid:{cpnyid}\n')
        sql = f"""select v.vip_id, v.vip_name,vl.label_name,vlg.color from vipinfo as v
join vip_label_stat as vs on v.vip_id = vs.vip_id
join vip_label as vl on vl.label_id = vs.label_id
join VIP_LABEL_GROUP vlg on vlg.label_gid = vl.label_gid  
where v.cpnyid='{cpnyid}' order by v.vip_id, vlg.label_gid ;"""
        conn = connect(**db_settings)
        cursor = conn.cursor()
        cursor.execute(sql)
        vip_label_data = {}
        for i in cursor:
            vip_id_name = i[0]+" "+i[1]
            if vip_id_name not in vip_label_data:
                vip_label_data[vip_id_name]=[]

            rows_data = {
                "label_name" : i[2],
                "color":i[3]
            }   
            vip_label_data[vip_id_name].append(rows_data)

        cursor.close()
        conn.close()
        vip_label_stat_obj=None
        context = {}

        vip_label_stat_obj = VIP_LABEL_STAT.objects.filter(cpnyid=cpnyid).first()
  
        if vip_label_stat_obj is None:
            context['no_data'] = True
            context['form'] = VIP_LABEL_STATModelForm()
            print(f'\ncontext:{context}\n')
        else:
            cpnyname = vip_label_stat_obj.cpnyid.cocname
            form = VIP_LABEL_STATModelForm(instance=vip_label_stat_obj)
            context = {'form':form,"vip_label_data":vip_label_data,'cpnyname':cpnyname}

        return render(request,'label_data/B02.html',context)

class B03View(View):
    vip_grp_form = VIP_LABEL_GROUP_ModelForm
    def get(self,request):
        
        context ={
            "vip_grp_form":self.vip_grp_form()
        }
        return render(request,'label_data/B03.html',context)
    def post(self,request):
        print(f'b03傳送資料:{request.POST}')
        print()

        label_grp_btn = False
        send_data = dict(request.POST)
        del send_data['csrfmiddlewaretoken']
        del send_data['cpnyid']
        if len(send_data)>0:
            label_grp_btn = list(send_data.keys())[0]

        cpnyid = request.POST.get('cpnyid')
        lab_grp_objs = VIP_LABEL_GROUP.objects.filter(cpnyid=cpnyid)
        if lab_grp_objs.count()==0:
            context ={
            "vip_grp_form":self.vip_grp_form(),
            "no_data":True
            }
            return render(request,'label_data/B03.html',context) 
        
        if VIP_LABEL_STAT.objects.filter(cpnyid=cpnyid).count()==0:
            context ={
            "vip_grp_form":self.vip_grp_form(),
            "no_data":True
            }
            return render(request,'label_data/B03.html',context)         

        print(f'lab_grp_objs:{lab_grp_objs}\n')
        print(f'send_data:{send_data}\n')
        lab_grp_data = VIP_LABEL_GROUP.objects.filter(cpnyid=cpnyid).first()
        if label_grp_btn :
            lab_grp_data = VIP_LABEL_GROUP.objects.filter(cpnyid=cpnyid,label_gid=label_grp_btn).first()

        context ={
            "vip_grp_form":self.vip_grp_form(instance=lab_grp_data)
        }
        print(f'cpnyid:{cpnyid}\n')

        # 畫面顯示品牌對應的標籤群組

        context["lab_grp_objs"] = lab_grp_objs

        first_lab_grp_objs = None
        if label_grp_btn :
            first_lab_grp_objs = list(lab_grp_objs.filter(label_gid=label_grp_btn))[0]
        else:
            first_lab_grp_objs = list(lab_grp_objs)[0]
        
        print(f'first_lab_grp_objs:{first_lab_grp_objs}\n')
        first_lab_objs = list(first_lab_grp_objs.vip_label_set.all())
        labels = []
        data = []
        print(f'first_lab_objs:{first_lab_objs}\n')
        for lab in first_lab_objs:
            labels.append(lab.label_name)
            data.append(lab.vip_label_stat_set.count())
        print(f'labels:{labels}\n')
        print(f'data:{data}\n')
        context["lab_labels"]=labels
        context["lab_data"]=data
        

        return render(request,'label_data/B03.html',context)



def d00005(conn,cursor,vip_id,cpnyid,calsdate,caledate):
    # 會員第一次交易日  
    sql = f"SELECT input_date FROM sales00 where vip_id='{vip_id}' and cpnyid = '{cpnyid}' and sale_status='1' and input_date between '{calsdate}' and '{caledate}' ORDER BY input_date LIMIT 1;"
    cursor.execute(sql)
    for i in cursor:
        return i[0]
    
def d00006(conn,cursor,vip_id,cpnyid,calsdate,caledate):
    # 會員最後一次交易日
  
    sql = f"SELECT input_date FROM sales00 where vip_id='{vip_id}' and cpnyid = '{cpnyid}' and sale_status='1' and input_date between '{calsdate}' and '{caledate}' ORDER BY input_date desc LIMIT 1;"
    cursor.execute(sql)
    for i in cursor:
        return i[0]
    
def d00007(conn,cursor,vip_id,cpnyid,calsdate,caledate):
    # 會員購買金額總和   
    sql = f"SELECT sum(tot_sales) FROM sales00 where vip_id='{vip_id}' and cpnyid = '{cpnyid}' and sale_status='1' and input_date between '{calsdate}' and '{caledate}' ;"
    cursor.execute(sql)
    for i in cursor:
        print(f'會員購買金額總和:{i[0]}')
        return i[0]

def d00008(conn,cursor,vip_id,cpnyid,calsdate,caledate):
    # 會員購買次數總和  
    sql = f"SELECT count(*) FROM sales00 where vip_id='{vip_id}' and cpnyid = '{cpnyid}' and sale_status='1' and input_date between '{calsdate}' and '{caledate}' ;"
    cursor.execute(sql)
    for i in cursor:
        return i[0]

def d00009(conn,cursor,vip_id,cpnyid,calsdate,caledate):
    # 會員單日最大消費金額  
    sql = f"SELECT tot_sales FROM sales00 where vip_id='{vip_id}' and cpnyid = '{cpnyid}' and sale_status='1' and input_date between '{calsdate}' and '{caledate}' order by tot_sales desc LIMIT 1;"
    cursor.execute(sql)
    for i in cursor:
        return i[0]

def d00010(conn,cursor,vip_id,cpnyid,calsdate,caledate):
    # 會員單日最低消費金額
  
    sql = f"SELECT tot_sales FROM sales00 where vip_id='{vip_id}' and cpnyid = '{cpnyid}' and sale_status='1' and input_date between '{calsdate}' and '{caledate}' order by tot_sales LIMIT 1;"
    
    cursor.execute(sql)
    for i in cursor:
        return i[0]

def d00011(conn,cursor,vip_id,cpnyid,calsdate,caledate):
    # 會員單日最低消費金額
  
    sql = f"SELECT count(*)  FROM sales00 where vip_id='{vip_id}' and cpnyid = '{cpnyid}' and sale_status='1' and input_date between '{calsdate}' and '{caledate}' GROUP BY input_date order by count(*) desc LIMIT 1;"
    cursor.execute(sql)
    for i in cursor:
        return i[0]

def d00012(conn,cursor,vip_id,cpnyid,calsdate,caledate):
    # 會員回購次數 = 會員購買次數總和 - 1
    return d00008(conn,cursor,vip_id,cpnyid,calsdate,caledate)-1

def d00013(conn,cursor,vip_id,cpnyid,calsdate,caledate):
    # 會員客單價 = 會員購買金額總和 / 會員購買次數總和
    try :
        return round(d00007(conn,cursor,vip_id,cpnyid,calsdate,caledate)/d00008(conn,cursor,vip_id,cpnyid,calsdate,caledate),2)   
    except:
        return 0
def d00014(conn,cursor,vip_id,cpnyid,calsdate,caledate):

    # 會員消費金額中位數 
  
    sql = f"SELECT tot_sales FROM sales00 where vip_id='{vip_id}' and cpnyid = '{cpnyid}' and sale_status='1' and input_date between '{calsdate}' and '{caledate}' order by tot_sales;"
    cursor.execute(sql)
    return np.median([i[0] for i in cursor])
    
def d00015(conn,cursor,vip_id,cpnyid,calsdate,caledate):
    # 會員消費金額標準差    
    sql = f"SELECT tot_sales FROM sales00 where vip_id='{vip_id}' and cpnyid = '{cpnyid}' and sale_status='1' and input_date between '{calsdate}' and '{caledate}' order by tot_sales;"
    cursor.execute(sql)
    return round(np.std([i[0] for i in cursor]),2) 
        
def d00016(conn,cursor,vip_id,cpnyid,calsdate,caledate): 
    #會員平均回購天數
    d6 = d00006(conn,cursor,vip_id,cpnyid,calsdate,caledate)
    d5 =  d00005(conn,cursor,vip_id,cpnyid,calsdate,caledate)
    d12 = d00012(conn,cursor,vip_id,cpnyid,calsdate,caledate)
    if d12!=0:
        return round(((d6-d5).days)/d12,2)
    else :
        return (caledate-d5).days
        
def d00017(conn,cursor,vip_id,cpnyid,calsdate,caledate):

    # 會員回購天數標準差 
   
    sql = f"SELECT input_date FROM sales00 where vip_id='{vip_id}' and cpnyid = '{cpnyid}' and sale_status='1' and input_date between '{calsdate}' and '{caledate}' order by input_date ;"
    cursor.execute(sql)
    input_date_list = [d[0] for d in cursor]
    re_purchase_list = []
    for i in range(len(input_date_list)-1):
        d = (input_date_list[i+1]-input_date_list[i]).days
        re_purchase_list.append(d)
    r = np.std(re_purchase_list)
    if str(r)=='nan':
        return (caledate-input_date_list[0]).days
    return round(r,2) 

def cpny_totsales(conn,cursor,cpnyid,calsdate,caledate):
    sql = f"SELECT tot_sales FROM sales00 where cpnyid = '{cpnyid}' and sale_status='1' and input_date between '{calsdate}' and '{caledate}';"
    cursor.execute(sql)   
    tot_sales_list = [t[0] for t in cursor]
    return {
        "median" : np.median(tot_sales_list),
        "std":round(np.std(tot_sales_list),2)
        }
    
param_dict = {
    "D00005":d00005,
    "D00006":d00006,
    "D00007":d00007,
    "D00008":d00008,
    "D00009":d00009,
    "D00010":d00010,
    "D00011":d00011,
    "D00012":d00012,
    "D00013":d00013,
    "D00014":d00014,
    "D00015":d00015,
    "D00016":d00016,
    "D00017":d00017,
    }

db_settings = {

}
with open('label_data/db_connect_config.txt','r') as f :
    line = f.readlines()
    for i in line :
        t =  i.replace('\n','')
        tmp = t.split(',')
        if tmp[0]=='port':
            db_settings[tmp[0]]=int(tmp[1])
        else:
            db_settings[tmp[0]]=(tmp[1])

class B04View(View):
    form = VIP_LABEL_STATModelForm2
    def get(self,request):
        context = {
            'form':self.form()
        }
        return render(request,'label_data/B04.html',context)
    
    def post(self,request):
        print(f'b04送post請求....')
        
        context={
            'form':self.form()
        }


        global db_settings
        global param_dict
        print(db_settings)
        conn = connect(**db_settings)
        cursor = conn.cursor()
        from  datetime import datetime
        cpnyid_val = request.POST.get('cpnyid')
        caledate = datetime.strptime(request.POST.get('caledate'), "%Y-%m-%d").date()

        print(f"計算日訖:{caledate}")
        
        # 抓會員參數
        # 1.取出所有品牌 cpnyid
        cursor.execute(f"select cpnyid from crm_company where cpnyid='{cpnyid_val}';")
        cpnyid_list =[i[0] for i in cursor]
        print(cpnyid_list)
        muser = 'admin'
        mdate = date.today()
        loc_dt = datetime.today() 
        loc_dt_format = loc_dt.strftime("%Y/%m/%d %H:%M:%S")
        mtime = loc_dt_format[11:]

        cpnyid_vip_params_dict = {}
        cpnyid_params_infos = {}

        # 2.逐一遍歷品牌
        for cpnyid in cpnyid_list:
            cpnyid_vip_params_dict[cpnyid]=[]
            d00018 = 0 # 品牌購買金額總和
            d00019 = 0 #品牌單日最大消費次數
            d00020 = 0 #品牌購買次數總和
            d00021 = 0 # 品牌單日最大消費金額
            d00022 = 0 # 品牌單日最低消費金額
            d00023 = 0 # 品牌最大購買金額總和
            d00024 = None # 品牌最低購買金額總和
            d00025 =0 # 品牌最大購買次數總和
            d00026 = None # 品牌最低購買次數總和
            d00027 = None # 品牌第一次交易日
            d00028 = None # 品牌最後一次交易日
            d00029 = 0 # 品牌平均消費金額
            
            cpny_repurchase_day_list = []
            print(f'cpnyid = {cpnyid}')
            cursor.execute(f"delete from paramater_stat where cpnyid ='{cpnyid}'")
            conn.commit()
            print(f'先刪除前一次參數')
            # 2.1 取出品牌的創立時間cdate作為 calsdate (計算日起)
            calsdate = CRM_COMPANY.objects.get(cpnyid=cpnyid).cdate
            print(f'calsdate = {calsdate}')
            # 取出所有vip_id
            cursor.execute(f"select vip_id from vipinfo where cpnyid ='{cpnyid}'")
            vip_id_list = [v[0] for v in cursor]
            print(f'len(vip_id_list) = {len(vip_id_list)}')
            if len(vip_id_list)==0:
                context['wrong']="該品牌還未有會員，因此無法執行貼標"
                return render(request,'label_data/B04.html',context)

            if Sales00.objects.filter(cpnyid=cpnyid).count()==0:
                context['wrong']="該品牌未有任何顧客消費紀錄，因此執行貼標無意義"
                return render(request,'label_data/B04.html',context)

            # 取出所有顧客參數
            cursor.execute(f"select PARAM_ID from PARAMATER where IS_BRAND ='N';")
            param_list = [p[0] for p in cursor]
            print(f'param_list = {(param_list)}')
            
            # 遍歷 vip_id_list
            for vip_id in vip_id_list:
                print("===================")
                print(f'vip_id:{vip_id}')
                tmp_vip_params = {"vip_id":vip_id}
                for param_id in param_list:
                    print(f'param_id:{param_id}')
                    get_param_fn_params = {"conn":conn,"cursor":cursor,"vip_id":vip_id,"cpnyid":cpnyid,"calsdate":calsdate,"caledate":caledate}
                    get_param_fn = param_dict[param_id]
                    param_value = get_param_fn(**get_param_fn_params)
                    if param_id == 'D00005':
                        if d00027 is None :
                            d00027 = param_value
                        else :
                            d00027 = param_value if param_value<d00027 else d00027
                    elif param_id == 'D00006':
                        if d00028 is None :
                            d00028 = param_value
                        else :
                            d00028 = param_value if param_value>d00028 else d00028               
                    elif param_id == 'D00007':
                        d00018+=int(param_value)
                        d00023 = param_value if param_value>d00023 else d00023
                        if d00024 is None :
                            d00024 = param_value
                        else :
                            d00024 = param_value if param_value<d00024 else d00024
                    elif  param_id == 'D00008':
                        d00020+=int(param_value)
                        d00025 = param_value if param_value>d00025 else d00025
                        if d00026 is None :
                            d00026 = param_value
                        else :
                            d00026 = param_value if param_value<d00026 else d00026
                    elif  param_id == 'D00009':
                        d00021 = param_value if param_value>d00021 else d00021
                    elif param_id == 'D00010':
                        d00022 = param_value if param_value>d00022 else d00022
                    elif param_id == 'D00011':
                        d00019 = param_value if param_value>d00019 else d00019
                    elif param_id == 'D00016':
                        cpny_repurchase_day_list.append(param_value)           
                    
                    print(f'param_value = {param_value}')

                    sql = f"""
        insert into paramater_stat(cpnyid,vip_id,param_id,param_value,muser,mdate,mtime)
        values('{cpnyid}','{vip_id}','{param_id}','{param_value}','{muser}','{mdate}','{mtime}')"""
                    cursor.execute(sql)
                    conn.commit()
                    tmp_vip_params[param_id]=param_value
                cpnyid_vip_params_dict[cpnyid].append(tmp_vip_params)
            
            d00029 = round((d00018/d00020),2)
            sss=cpny_totsales(conn,cursor,cpnyid,calsdate,caledate)
            d00030 =sss['median'] #品牌消費金額中位數
            d00031 =sss['std'] #品牌消費金額標準差
            d00032 = np.median(cpny_repurchase_day_list)
            d00033 = round(np.std(cpny_repurchase_day_list),2)
            param_cpny_dict = {
                "D00002":caledate,
                "D00018":d00018,
                "D00019":d00019,
                "D00020":d00020,
                "D00021":d00021,
                "D00022":d00022,
                "D00023":d00023,
                "D00024":d00024,
                "D00025":d00025,
                "D00026":d00026,
                "D00027":d00027,
                "D00028":d00028,
                "D00029":d00029,
                "D00030":d00030,
                "D00031":d00031,
                "D00032":d00032,
                "D00033":d00033,
                }    
            
            # 取出所有顧客參數
            cursor.execute(f"select PARAM_ID from PARAMATER where IS_BRAND ='Y';")
            param_cpny_list = [p[0] for p in cursor]
            cursor.execute(f"delete from paramater_stat_company where cpnyid ='{cpnyid}'")
            conn.commit()
            print(f'先刪除前一次參數')
            for param_id in param_cpny_list:
                param_value = param_cpny_dict[param_id]
                sql = f"""
        insert into paramater_stat_company(cpnyid,param_id,param_value,muser,mdate,mtime)
        values('{cpnyid}','{param_id}','{param_value}','{muser}','{mdate}','{mtime}')"""
                cursor.execute(sql)
                conn.commit()        
                
            print(f'param_cpny_list = {(param_cpny_list)}')
            cpnyid_params_infos[cpnyid]=param_cpny_dict


        print("顧客參數完成˙!")

        # 計算出貼標公式的結果值
        #取出公式
        cursor.execute(f"select formula_id,formula_rule from Formula;")

        formula_infos = [{"formula_id":f[0],"formula_rule":f[1]} for f in cursor]
        print(formula_infos)
        cpnyid_vip_formula_dict = {}
        import re

        for cpnyid in cpnyid_list:
            cursor.execute(f"delete from vip_formula_stat where cpnyid ='{cpnyid}'")
            conn.commit()
            print(f'先刪除前一次參數')
            cpnyid_vip_formula_dict[cpnyid]=[]
            cpnyid_params_dict = cpnyid_params_infos[cpnyid]
            for vip in cpnyid_vip_params_dict[cpnyid]:
                tmp_vip_formula_dict = {}
                vip_id = vip['vip_id']
                tmp_vip_formula_dict['vip_id']=vip_id
                for f_infos in formula_infos:
                    formula_id = f_infos['formula_id']
                    formula_rule = f_infos['formula_rule']
                    print(f'formula_id:{formula_id}')
                    pat = '\w+'
                    r = re.findall(pat, formula_rule)
                    for i in r :
                        ans=''
                        if i in vip:
                            ans = str(vip[i])
                        else:
                            ans = str(cpnyid_params_dict[i])
                        formula_rule = formula_rule.replace(f'[{i}]',ans)
                    print(f'formula_rule=>{formula_rule}')
                
                    pat1 = '\d{4}-\d{2}-\d{2}-\d{4}-\d{2}-\d{2}'
                    r1 = re.findall(pat1, formula_rule)
                    if len(r)>0:
                        for i in r1 :
                            pat2 = '\d{4}-\d{2}-\d{2}'
                            r2 = re.findall(pat2, i)
                            d1 = datetime.strptime(r2[0], "%Y-%m-%d").date()
                            d2 = datetime.strptime(r2[1], "%Y-%m-%d").date()
                            diff = str((d1-d2).days)
                            formula_rule = formula_rule.replace(i,diff)
                            print(f'formula_rule=>{formula_rule}')
                    result_value = round(eval(formula_rule),2)
                    if formula_id == 'D02' and result_value== 0.0:
                        result_value = round(((caledate-vip['D00005']).days)/cpnyid_params_dict["D00032"],2)
                    print(f'result_value:{result_value}')
                    tmp_vip_formula_dict[formula_id]=result_value
                    cursor.execute(f"""
        insert into vip_formula_stat(cpnyid,vip_id,formula_id,result_value,muser,mdate,mtime) 
        values('{cpnyid}','{vip_id}','{formula_id}','{result_value}','{muser}','{mdate}','{mtime}')""")
                    conn.commit()
                cpnyid_vip_formula_dict[cpnyid].append(tmp_vip_formula_dict)

        print("顧客公式計算完成˙!")

        # 貼標
        for cpnyid in cpnyid_list:
            cursor.execute(f"delete from VIP_LABEL_STAT where cpnyid ='{cpnyid}'")
            conn.commit()
            print(f'先刪除前一次參數')    
            # 2.1 取出品牌的創立時間cdate作為 calsdate (計算日起)
            cursor.execute(f"select cdate from crm_company where cpnyid ='{cpnyid}'")
            calsdate = [c[0] for c in cursor][0]
            cursor.execute(f"select label_gid,formula_id,isxor from VIP_LABEL_GROUP where cpnyid='{cpnyid}';")
            vip_grp_label = [{"label_gid":i[0],"formula_id":i[1],"xor":i[2]} for i in cursor]
            if len(vip_grp_label)==0:
                context['wrong']="該品牌還未定義標籤"
                return render(request,'label_data/B04.html',context)

            for label_gid_obj in vip_grp_label:
                label_gid = label_gid_obj["label_gid"]
                formula_id = label_gid_obj['formula_id']
                isxor = label_gid_obj['xor']
                cursor.execute(f"select label_id,calmin,calmax from VIP_LABEL where label_gid='{label_gid}';")
                vip_label = [{'label_id':i[0],"calmin":i[1],"calmax":i[2]} for i in cursor]
                for vip in cpnyid_vip_formula_dict[cpnyid]:
                    vip_id = vip['vip_id']
                    formula_val = vip[formula_id] 
                    for label_obj in vip_label:
                        label_id = label_obj["label_id"]
                        calmin = float(label_obj['calmin'])
                        calmax = float(label_obj['calmax']) 
                        if calmin<=formula_val<=calmax:
                            cursor.execute(f"""insert into VIP_LABEL_STAT(cpnyid,vip_id,label_id,calsdate,caledate,muser,mdate,mtime)
        value('{cpnyid}','{vip_id}','{label_id}','{calsdate}','{caledate}','{muser}','{mdate}','{mtime}')                               
        """)
                            conn.commit()
                            print(f'vip {vip_id} 的公式值 {formula_val}介於 {calmin}~{calmax}  因此貼上 {label_id}')
                            if isxor =='1':
                                break

        context['success']="貼標完成"
        print("貼標完成")
        cursor.close()
        conn.close()
        return render(request,'label_data/B04.html',context)
