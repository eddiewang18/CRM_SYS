from django.shortcuts import render,redirect
from django.views import View
from .models import CRM_COMPANY
from .forms import CRM_COMPANY_ModelForm
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import JsonResponse
import json
# Create your views here.
class A01View(View):
    def get(self,request):
        form = CRM_COMPANY_ModelForm()
    
        context = {
            'form':form
        }
        return render(request,'basic_data/A01.html',context)
    
    def post(self,request):

        if 'create' in request.POST:
            form = CRM_COMPANY_ModelForm(data=request.POST)
            context = {
                'form':form
            }
            if form.is_valid():
                cpny = form.save(commit=False)
                cpny.muser = request.user.username
                cpny.save()
                context['success']="成功儲存"
                context['form']=CRM_COMPANY_ModelForm()
                return render(request,'basic_data/A01.html',context)
            
            context['wrong']=form.errList[0]
            return render(request,'basic_data/A01.html',context)
        elif 'query' in request.POST:
            form = CRM_COMPANY_ModelForm()
            context = {
                'form':form,
                'queryModal':True
            }
            

            return render(request,'basic_data/A01.html',context)

        # elif "querySubmit" in request.POST:
        #     # print(f'request.POST : {request.POST}')
        #     requestData = json.loads(request.POST.get("requestData"))
        #     print(f'{requestData}\n{type(requestData)}\n')
        #     # cols = ['cpnyid','cocname','coename','coscname','cosename']
        #     cols = ['cpnyid','cocname','coename']
        #     result_query = list(CRM_COMPANY().crmQdata(requestData).values(*cols))
        #     print(result_query)



        #     return JsonResponse(result_query,safe=False)

        # 用axios發送post
        elif "querySubmit" in  json.loads(request.body.decode('utf-8'))['params']:
            
            # print(f'request.POST : {request.POST}')
            requestData =json.loads(json.loads(request.body.decode('utf-8'))['params']['requestData'])
            # print(f'{requestData}\n{type(requestData)}\n')
            cols = ['cpnyid','cocname','coename','coscname','cosename']
            # cols = ['cpnyid','cocname','coename']
            result_query = list(CRM_COMPANY().crmQdata(requestData).values(*cols))
            # print(result_query)

            return JsonResponse(result_query,safe=False)
        elif "delete" in  json.loads(request.body.decode('utf-8'))['params']:
            print("\n==========delete==========\n")

            requestData =json.loads(request.body.decode('utf-8'))
            pk_fields = json.loads(requestData['params']['pk_fields']) 
            print(f'pk_fields : {pk_fields} | pk_fields type :{type(pk_fields)}')
            del_instance = CRM_COMPANY().crmQdata(pk_fields)[0]
            print(del_instance)
            del_instance.delete()
            # print("\ndelete OK\n")
            return JsonResponse({})

    def put(self,request):
        print()
        requestData =json.loads(request.body.decode('utf-8'))
        pk_fields = json.loads(requestData['params']['pk_fields']) 
        print(f'pk_fields : {pk_fields}')
        updata_data = json.loads(requestData['params']['updateData'])
        updated_instance = CRM_COMPANY().crmQdata(pk_fields)[0]
        print(f'updated_instance : {updated_instance}')
        form = CRM_COMPANY_ModelForm(instance=updated_instance,data=updata_data)
        context = {
            'form':form,
            'queryModal':True
        }
        if form.is_valid():
            
            # context['success']="成功儲存"
            context['form']=CRM_COMPANY_ModelForm()
            form.save()

            return JsonResponse({"update":"success"})
        wrongMsg=form.errList[0]
        print("表單驗證有誤")

        return JsonResponse({"update":"fail","wrongMsg":wrongMsg})


@receiver(pre_save,sender=CRM_COMPANY)
def crm_company_pre_save(instance,**kwargs):
    cpnyid = instance.pk 
    print(instance)
    data_exists =  CRM_COMPANY.objects.filter(cpnyid=cpnyid).exists()
    if not data_exists:
        instance.cuser = instance.muser
    

