from django.shortcuts import render
from basic_data.views import (
    dataCuser,
    FnView
)
from django.views import View
from .models import (
    VIP_LABEL_GROUP,
    VIP_LABEL,
    VIP_LABEL_STAT
)
from .forms import (
    VIP_LABEL_GROUP_ModelForm,
    VIP_LABEL_GROUP_QModelForm,
    VIP_LABEL_ModelForm,
    VIP_LABEL_STATModelForm
)
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import JsonResponse
import json
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
    def get(self,request):
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

