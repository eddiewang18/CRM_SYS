from django.shortcuts import render,redirect
from django.views import View
from .models import CRM_COMPANY
from .forms import CRM_COMPANY_ModelForm,SHOPGROUP_ModelForm
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import JsonResponse
import json
# Create your views here.
# class A01View(View):
#     def get(self,request):
#         form = CRM_COMPANY_ModelForm()
    
#         context = {
#             'form':form
#         }
#         return render(request,'basic_data/A01.html',context)
    
#     def post(self,request):

#         if 'create' in request.POST:
#             form = CRM_COMPANY_ModelForm(data=request.POST)
#             context = {
#                 'form':form
#             }
#             if form.is_valid():
#                 cpny = form.save(commit=False)
#                 cpny.muser = request.user.username
#                 cpny.save()
#                 context['success']="成功儲存"
#                 context['form']=CRM_COMPANY_ModelForm()
#                 return render(request,'basic_data/A01.html',context)
            
#             context['wrong']=form.errList[0]
#             return render(request,'basic_data/A01.html',context)
#         elif 'query' in request.POST:
#             form = CRM_COMPANY_ModelForm()
#             context = {
#                 'form':form,
#                 'queryModal':True
#             }
            

#             return render(request,'basic_data/A01.html',context)

#         # elif "querySubmit" in request.POST:
#         #     # print(f'request.POST : {request.POST}')
#         #     requestData = json.loads(request.POST.get("requestData"))
#         #     print(f'{requestData}\n{type(requestData)}\n')
#         #     # cols = ['cpnyid','cocname','coename','coscname','cosename']
#         #     cols = ['cpnyid','cocname','coename']
#         #     result_query = list(CRM_COMPANY().crmQdata(requestData).values(*cols))
#         #     print(result_query)



#         #     return JsonResponse(result_query,safe=False)

#         # 用axios發送post
#         elif "querySubmit" in  json.loads(request.body.decode('utf-8'))['params']:
            
#             # print(f'request.POST : {request.POST}')
#             requestData =json.loads(json.loads(request.body.decode('utf-8'))['params']['requestData'])
#             # print(f'{requestData}\n{type(requestData)}\n')
#             cols = ['cpnyid','cocname','coename','coscname','cosename']
#             # cols = ['cpnyid','cocname','coename']
#             result_query = list(CRM_COMPANY().crmQdata(requestData).values(*cols))
#             # print(result_query)

#             return JsonResponse(result_query,safe=False)
#         elif "delete" in  json.loads(request.body.decode('utf-8'))['params']:
#             print("\n==========delete==========\n")

#             requestData =json.loads(request.body.decode('utf-8'))
#             pk_fields = json.loads(requestData['params']['pk_fields']) 
#             print(f'pk_fields : {pk_fields} | pk_fields type :{type(pk_fields)}')
#             del_instance = CRM_COMPANY().crmQdata(pk_fields)[0]
#             print(del_instance)
#             del_instance.delete()
#             # print("\ndelete OK\n")
#             return JsonResponse({})

#     def put(self,request):
#         print()
#         requestData =json.loads(request.body.decode('utf-8'))
#         pk_fields = json.loads(requestData['params']['pk_fields']) 
#         print(f'pk_fields : {pk_fields}')
#         updata_data = json.loads(requestData['params']['updateData'])
#         updated_instance = CRM_COMPANY().crmQdata(pk_fields)[0]
#         print(f'updated_instance : {updated_instance}')
#         form = CRM_COMPANY_ModelForm(instance=updated_instance,data=updata_data)
#         context = {
#             'form':form,
#             'queryModal':True
#         }
#         if form.is_valid():
            
#             # context['success']="成功儲存"
#             context['form']=CRM_COMPANY_ModelForm()
#             form.save()

#             return JsonResponse({"update":"success"})
#         wrongMsg=form.errList[0]
#         print("表單驗證有誤")

#         return JsonResponse({"update":"fail","wrongMsg":wrongMsg})


def dataCuser(model):
    @receiver(pre_save,sender=model)
    def cuser_pre_save(instance,**kwargs):
        pk_field = instance.pk 
        data_exists =  model.objects.filter(pk=pk_field).exists()
        if not data_exists:
            instance.cuser = instance.muser
dataCuser(CRM_COMPANY)

    
class FnView(View):
    """
    屬性:
        model :  開發功能對應的 Model
        model_form : 開發功能對應的 ModelForm
        html_file :  開發功能對應的html頁面
        return_query_cols : 查詢時要返回的欄位資料，以list的類別儲存 e.g. [col1,col2,.....]

    """
    def get(self,request):
        """
        get 方法返回ModelForm空白欄位表單
        """
        form = self.model_form()
        context = {
            'form':form
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
            form = self.model_form(data=request.POST)
            context = {
                'form':form
            }
            if form.is_valid():
                table_data = form.save(commit=False)
                table_data.muser = request.user.username
                table_data.save()
                context['success']="成功儲存"  
                context['form']=self.model_form()
                return render(request,self.html_file,context)
            
            context['wrong']=form.errList[0]
            return render(request,self.html_file,context)
        elif 'query' in request.POST:
            form = self.model_form()
            context = {
                'form':form,
                'queryModal':True
            }
        
            return render(request,self.html_file,context)

        # 用axios發送post
        elif "querySubmit" in  json.loads(request.body.decode('utf-8'))['params']:
            requestData =json.loads(json.loads(request.body.decode('utf-8'))['params']['requestData'])
            result_query = list(self.model().crmQdata(requestData).values(*self.return_query_cols ))
            return JsonResponse(result_query,safe=False)
        elif "delete" in  json.loads(request.body.decode('utf-8'))['params']:
            requestData =json.loads(request.body.decode('utf-8'))
            pk_fields = json.loads(requestData['params']['pk_fields']) 
            del_instance = self.model().crmQdata(pk_fields)[0]
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
        updated_instance = self.model().crmQdata(pk_fields)[0]
        form = self.model_form(instance=updated_instance,data=updata_data)
        context = {
            'form':form,
            'queryModal':True
        }
        if form.is_valid():
            context['form']=self.model_form()
            form.save()
            return JsonResponse({"update":"success"})
        wrongMsg=form.errList[0]

        return JsonResponse({"update":"fail","wrongMsg":wrongMsg})


class A01View(FnView):
    model = CRM_COMPANY
    model_form = CRM_COMPANY_ModelForm
    html_file = 'basic_data/A01.html'
    return_query_cols = ['cpnyid','cocname','coename','coscname','cosename']


class A02View(View):
    def get(self,request):
        form = SHOPGROUP_ModelForm()
        context = {
            'form':form
        }
        return render(request,'basic_data/A02.html',context)

    def post(self,request):
        print('\na02 post\n')
        data = json.loads(request.POST.get("postData")) 
        insert_data = data.get("insert") # [{'shopgroup_id': 'wdf', 'shopgroup_name': '123'}, {'shopgroup_id': 'ewq', 'shopgroup_name': '234'}]
        update_data = data.get("update")
        delete_data = data.get('delete')
        print(f'\ninsert_data : {insert_data}\n')
        print(f'\nupdate_data : {update_data}\n')
        print(f'\ndelete_data : {delete_data}\n')

        return JsonResponse({"update":"ok"})


