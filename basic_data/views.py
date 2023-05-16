from django.shortcuts import render,redirect
from django.views import View
from .models import (CRM_COMPANY,SHOPGROUP,SHOP,County,Area,HRUSER_GROUP,CRM_HRUSER,VIPINFO_GROUP)
from .forms import (
    CRM_COMPANY_ModelForm,SHOPGROUP_ModelForm,SHOP_ModelForm,SHOP_QModelForm
    ,CRM_COMPANY_QModelForm,HRUSER_GROUP_ModelForm,CRM_HRUSER_ModelForm,CRM_HRUSER_QModelForm,VIPINFO_GROUP_ModelForm
)
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import JsonResponse
import json
# Create your views here.

# 將每一列資料指定的choices欄位轉成human readable的欄位值
def turnChoiceField2readable(data,choicesInfo:list):
    """
    data > queryset type , 格式 : [{col1:value1,col2:value2,....},{col1:value1,col2:value2,....}]
    choices_belong_model > choices所屬的model
    choices_attr_name > choices的屬性名
    choices_field_name > 要轉成readale的choices欄位名
    [{'choices_belong_model':SHOP,"choices_attr_name":"shop_kind_choices","choices_field_name":shop_kind},{}]
    """
    def get_readable_choicefield(model,choices_attr,choice_value):
        try :
            if choice_value :
                choicesList = getattr(model,choices_attr)
                for choice in choicesList:
                    if choice[0]==choice_value:
                        return choice[1]
            return ''
        except :
            print(f"在{model}中找不到屬性{choices_attr}")
    for i in data:
        for info in choicesInfo:
            label_name= get_readable_choicefield(info['choices_belong_model'],info['choices_attr_name'],i[info['choices_field_name']])
            i[info['choices_field_name']]=label_name

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
        query_model_form : 開發功能按查尋按鈕時跳出來對應的查詢表單欄位
        result_model_form  : 開發功能結果顯示時跳出來對應的表單欄位
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
            # result_query = list(self.model().crmQdata(requestData).values())
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

def county_area(request):
    if 'county_id' in request.GET:
        county_id = request.GET.get('county_id')
        post_objs = list(Area.objects.filter(county_id=county_id).values("post_id","post_name"))
        return JsonResponse(post_objs,safe=False)

# def county_area(request):
#     if 'change_select_ele' in request.GET:
#         print("\nchange_select_ele\n")
#         county_id = request.GET.get('change_select_ele')
#         post_objs = list(Area.objects.filter(county_id=county_id).values("post_id","post_name"))
#         return JsonResponse(post_objs,safe=False)

class A01View(FnView):
    model = CRM_COMPANY
    model_form = CRM_COMPANY_ModelForm
    query_model_form = CRM_COMPANY_QModelForm
    # verbose_name_fields = model_form.verbose_name_fields
    verbose_name_fields = model_form().verbose_name_fields

    html_file = 'basic_data/A01.html'
    # return_query_cols = model_form.return_query_cols
    return_query_cols = model_form().return_query_cols

class A03View(FnView):
    model = SHOP
    model_form = SHOP_ModelForm
    query_model_form = SHOP_QModelForm
    # verbose_name_fields = model_form.verbose_name_fields
    verbose_name_fields = model_form().verbose_name_fields
    html_file = 'basic_data/A03.html'
    # return_query_cols = model_form.return_query_cols
    return_query_cols = model_form().return_query_cols



class Fn2View(View):
    """
    主表搭配副表的功能

    屬性:
        model :  開發功能對應的 Model
        model_form : 開發功能對應的 ModelForm
        html_file :  開發功能對應的html頁面
        fk_attr : str類型,主表對應副表的相關資料集合，以 副表小寫_set 的形式表現 
        fk_cols_show_list : list類型，儲存前台畫面中副表要呈現的欄位
        choice2readableInfos : list類型，將副表中為下拉選單的欄位依依轉換為易讀的值，一個下拉選單的欄位以dict型態分別存入在choice2readableInfos中
        cols_show_list : list類型，儲存前台畫面中主表要呈現的欄位
    """
    def get(self,request):
        
        if 'switch' in request.GET :
            requestData = json.loads(request.GET.get('postData')) 
            # shopgroup_id = requestData.get('pk')
            primary_key =  requestData.get('pk')
            # shopgroup_obj = SHOPGROUP.objects.get(pk = shopgroup_id)
            main_obj = self.model.objects.get(pk = primary_key)
            included_fk_objs = getattr(main_obj,self.fk_attr).all().values(*self.fk_cols_show_list)
            # included_shop_objs =  shopgroup_obj.shop_set.all().values('shop_id','shop_name','shop_kind','cpnyid__cocname')
            # choice2readableInfos = [{'choices_belong_model':SHOP,"choices_attr_name":"shop_kind_choices","choices_field_name":'shop_kind'}]
            # turnChoiceField2readable(included_shop_objs,choice2readableInfos)
            turnChoiceField2readable(included_fk_objs,self.choice2readableInfos)

            # print(included_shop_objs)
            return JsonResponse(list(included_fk_objs),safe=False)

        if 'query_condition' in request.GET :
            print('\nquery_condition\n')
            requestData = json.loads(request.GET.get('postData')) 
            print(f'\nrequestData:{requestData}|type : {type(requestData)}\n')
            # qs_result = list(SHOPGROUP().crmQdata(requestData,self.model.fk_list).values("shopgroup_id","shopgroup_name"))
            qs_result = list(self.model().crmQdata(requestData,self.model.fk_list).values(*self.cols_show_list))

            print(f'\nqs_result:{qs_result}\n')
            return JsonResponse(qs_result,safe=False)

        # form = SHOPGROUP_ModelForm()
        form = self.model_form()
        # objs = SHOPGROUP.objects.all()

        objs = self.model.objects.all().order_by(self.query_order)
        included_fk_objs=[]
        if len(objs)>0:
            first_obj = objs.first()
        # cpnyid__cocname > 使用 foreignkey__關聯model某屬性 可以讓該屬性做為顯示的資料
        # included_shop_objs = first_obj.shop_set.all().values('shop_id','shop_name','shop_kind','cpnyid__cocname')
            included_fk_objs = getattr(first_obj,self.fk_attr).all().values(*self.fk_cols_show_list)
        # choice2readableInfos = [{'choices_belong_model':SHOP,"choices_attr_name":"shop_kind_choices","choices_field_name":'shop_kind'}]
            turnChoiceField2readable(included_fk_objs,self.choice2readableInfos)
        # print()
        # print(included_shop_objs)
            objs = objs.values(*self.cols_show_list).order_by(self.query_order)
        context = {
            'form':form,
            'objs':objs,
            'included_fk_objs':included_fk_objs
        }

        if 'query' in request.GET :
            context['queryModal']=True
        # return render(request,'basic_data/A02.html',context)
        return render(request,self.html_file,context)

    def post(self,request):
        print('\na02 post\n')
        data = json.loads(request.POST.get("postData")) 
        insert_data = data.get("insert") # [{'shopgroup_id': 'wdf', 'shopgroup_name': '123'}, {'shopgroup_id': 'ewq', 'shopgroup_name': '234'}]
        update_data = data.get("update")
        delete_data = data.get('delete')
        print(f'\ninsert_data : {insert_data}\n')
        print(f'\nupdate_data : {update_data}\n')
        print(f'\ndelete_data : {delete_data}\n')
        if len(delete_data)>0:
            for data_row in delete_data:
                self.model.objects.get(pk=data_row[self.pk_key]).delete()
                # print(f'\ndelete a row\n')

        if len(insert_data)>0:
            for data_row in insert_data:
                form = self.model_form(data=data_row)
                if form.is_valid():
                    table_data = form.save(commit=False)
                    table_data.muser = request.user.username
                    table_data.save()
                    print(f'\ncreate a new row\n')
                else:
                    pass
                    print(f'\nform.errors :{form.errors}\n')
        
        if len(update_data)>0:
            for data_row in update_data:
                obj =self.model.objects.get(pk=data_row[self.pk_key])
                form =  self.model_form(instance=obj,data=data_row)
                if form.is_valid():
                    table_data = form.save(commit=False)
                    table_data.muser = request.user.username
                    table_data.save()
                    # print(f'\nupdate a row\n')
                else:
                    # print(f'\nform.errors :{form.errors}\n')
                    pass
        return JsonResponse({"update":"ok"})

class A02View(Fn2View):
    model = SHOPGROUP
    model_form = SHOPGROUP_ModelForm
    html_file = 'basic_data/A02.html'
    fk_attr = 'shop_set'
    fk_cols_show_list = ['shop_id','shop_name','shop_kind','cpnyid__cocname']
    choice2readableInfos =  [{'choices_belong_model':SHOP,"choices_attr_name":"shop_kind_choices","choices_field_name":'shop_kind'}]
    cols_show_list = ['shopgroup_id','shopgroup_name']
    pk_key = 'shopgroup_id'
    query_order = 'shopgroup_id'
dataCuser(SHOPGROUP)

class A04View(Fn2View):
    model = HRUSER_GROUP
    model_form = HRUSER_GROUP_ModelForm
    html_file = 'basic_data/A04.html'
    fk_attr = 'crm_hruser_set'
    fk_cols_show_list = ['empid','cname','shop_id__shop_name','cpnyid__cocname']
    choice2readableInfos =  []
    cols_show_list = ['group_id','group_name']
    pk_key = 'group_id'
    query_order = 'group_id'
dataCuser(HRUSER_GROUP)



def cpnyid_shop(request):
    if 'cpnyid' in request.GET:
        cpnyid = request.GET.get('cpnyid')
        shop_objs = list(SHOP.objects.filter(cpnyid=cpnyid).values("shop_id","shop_name"))
        return JsonResponse(shop_objs,safe=False)



class A05View(FnView):
    model = CRM_HRUSER
    model_form = CRM_HRUSER_ModelForm
    query_model_form = CRM_HRUSER_QModelForm
    verbose_name_fields = model_form().verbose_name_fields
    html_file = 'basic_data/A05.html'
    return_query_cols = model_form().return_query_cols


class A06View(Fn2View):
    model = VIPINFO_GROUP
    model_form = VIPINFO_GROUP_ModelForm
    html_file = 'basic_data/A06.html'
    fk_attr = 'vipinfo_set'
    fk_cols_show_list = ['vip_id','vip_name','shop_id__shop_name']
    choice2readableInfos =  []
    cols_show_list = ['vipinfo_group_id','vipinfo_group_name',"cpnyid"]
    pk_key = 'vipinfo_group_id'
    query_order = 'vipinfo_group_id'


    def get(self,request):
        
        if 'switch' in request.GET :
            requestData = json.loads(request.GET.get('postData')) 
            primary_key =  requestData.get('pk')
            main_obj = self.model.objects.get(pk = primary_key)
            included_fk_objs = getattr(main_obj,self.fk_attr).all().values(*self.fk_cols_show_list)
            turnChoiceField2readable(included_fk_objs,self.choice2readableInfos)
            return JsonResponse(list(included_fk_objs),safe=False)

        if 'query_condition' in request.GET :
            print('\nquery_condition\n')
            requestData = json.loads(request.GET.get('postData')) 
            print(f'\nrequestData:{requestData}|type : {type(requestData)}\n')
            qs_result = list(self.model().crmQdata(requestData,self.model.fk_list).values(*self.cols_show_list))

            print(f'\nqs_result:{qs_result}\n')
            return JsonResponse(qs_result,safe=False)
        form = self.model_form()
        objs = self.model.objects.all().order_by(self.query_order)
        included_fk_objs=[]
        if len(objs)>0:
            first_obj = objs.first()
            included_fk_objs = getattr(first_obj,self.fk_attr).all().values(*self.fk_cols_show_list)
            turnChoiceField2readable(included_fk_objs,self.choice2readableInfos)
            objs = objs.values(*self.cols_show_list).order_by(self.query_order)
        context = {
            'form':form,
            'objs':objs,
            'included_fk_objs':included_fk_objs
        }

        if 'query' in request.GET :
            context['queryModal']=True

        cpny_options = []
        for cpny_data in list(CRM_COMPANY.objects.all().values("cpnyid","cocname")):
            cpny_options.append({"value":cpny_data["cpnyid"],"label":cpny_data["cocname"]})
        context['cpny_options']= json.dumps(cpny_options,ensure_ascii=False) 
        print(context['cpny_options'])
        print(type(context['cpny_options']))
        return render(request,self.html_file,context)

dataCuser(VIPINFO_GROUP)