from django.shortcuts import render
from basic_data.views import (
    dataCuser,
    FnView
)
from django.views import View
from .models import (
    VIP_LABEL_GROUP,
    VIP_LABEL
)
from .forms import (
    VIP_LABEL_GROUP_ModelForm,
    VIP_LABEL_GROUP_QModelForm,
    VIP_LABEL_ModelForm
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

    def put(self,request):
        """
            put 方法:
                用於修改指定的數據
        """
        requestData =json.loads(request.body.decode('utf-8'))
        pk_fields = json.loads(requestData['params']['pk_fields']) 
        updata_data = json.loads(requestData['params']['updateData'])
        
        updated_instance = self.model().crmQdata(pk_fields,self.model.fk_list)[0]
        # print(f"\n更新資料:{updata_data}\n")
        # print(f'\n更新物件:{updated_instance}\n')
        form = self.model_form(instance=updated_instance,data=updata_data)
        context = {
            'form':form,
            'queryModal':True
        }
        if form.is_valid():
            context['form']=self.model_form()
            form.save()
            return JsonResponse({"update":"success"})
        # else:
        #     print(f'\n未通過表單驗證的原因:{form.errors.as_data()}\n')
        wrongMsg = ''
        if len(form.errList)>0:
            wrongMsg=form.errList[0]

        return JsonResponse({"update":"fail","wrongMsg":wrongMsg})

class B01View(FnTableView):
    model = VIP_LABEL_GROUP
    model_form = VIP_LABEL_GROUP_ModelForm
    table_form =  VIP_LABEL_ModelForm
    query_model_form = VIP_LABEL_GROUP_QModelForm
    verbose_name_fields = model_form().verbose_name_fields
    html_file = 'label_data/B01.html'
    return_query_cols = model_form().return_query_cols
    form_table_associate_key = 'label_gid'
    sub_model = VIP_LABEL
    sub_table_show_cols = ["label_id","label_name","calmin","calmax","label_enable"]

dataCuser(VIP_LABEL_GROUP)