from .models import CRM_COMPANY,SHOPGROUP,SHOP,Area
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

def give_form_general_class_attr(fields:dict):
    for name,field in fields.items():
        field.widget.attrs = {"class":"form_field"}


class CRM_COMPANY_ModelForm(ModelForm):
    verbose_name_fields = []
    return_query_cols = []
    for i in CRM_COMPANY._meta.get_fields(): 
        try:
            verbose_name_fields.append(i.verbose_name)
            return_query_cols.append(i.name)
        except:
            continue
    class Meta :
        model=CRM_COMPANY
        fields = ["cpnyid","cocname","coename","coscname","cosename"]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.errList = []
        give_form_general_class_attr(self.fields)
        self.fields['cpnyid'].widget.attrs.update({'class': 'pkField'}) #為某個欄位加上class屬性值




    def clean_cpnyid(self):
        cpnyid = self.cleaned_data.get("cpnyid")
        data_exists = None
        if not self.instance.pk :
            data_exists = CRM_COMPANY.objects.filter(cpnyid=cpnyid).exists()
        else:
            data_exists = CRM_COMPANY.objects.filter(cpnyid=cpnyid).exclude(cpnyid=cpnyid).exists()
        if data_exists :
            errMsg = f"公司編號 {cpnyid} 已存在 不可重複輸入"
            self.errList.append(errMsg)
            raise ValidationError(errMsg)
        else:
            return cpnyid


    
    def clean_cocname(self):
        cocname = self.cleaned_data.get("cocname")
        cpnyid = self.cleaned_data.get("cpnyid")
        data_exists = None
        if not self.instance.pk :
            data_exists = CRM_COMPANY.objects.filter(cocname=cocname).exists()
        else:
            data_exists = CRM_COMPANY.objects.filter(cocname=cocname).exclude(cpnyid=cpnyid).exists()


        if data_exists :
            errMsg = f"公司中文名稱 {cocname} 已存在 不可重複輸入"
            self.errList.append(errMsg)
            raise ValidationError(errMsg)
        else:
            return cocname 
        

class SHOPGROUP_ModelForm(ModelForm):
    class Meta :
        model=SHOPGROUP
        fields = ["shopgroup_id","shopgroup_name"]



class SHOP_ModelForm(ModelForm):
    verbose_name_fields = []
    return_query_cols = []
    for i in SHOP._meta.get_fields(): 
        try:
            verbose_name_fields.append(i.verbose_name)
            return_query_cols.append(i.name)
        except:
            continue

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["shop_disable_date"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields['shop_disable_date'].widget.attrs.update({'disabled': 'true'}) #為某個欄位加上class屬性值
        give_form_general_class_attr(self.fields)
        self.errList = []

        self.fields["post_id"].queryset= Area.objects.none()
        if "county_id" in self.data:
            try:
                county_id = self.data.get("county_id")
                self.fields["post_id"].queryset= Area.objects.filter(county_id=county_id)
            except:
                pass
        elif self.instance.pk:
            print(f'\n{self.fields["post_id"].queryset}\n')
            print(f'\n{self.instance}\n')
            print(f'\n{self.instance.county_id}\n')
            print(f'\n{self.instance.county_id.area_set.all()}\n')
            self.fields["post_id"].queryset= self.instance.county_id.area_set.all()        

    class Meta :
        model=SHOP
        fields = ["cpnyid","shop_id","shop_name",
        "shop_scname","shop_kind","shopgroup_id",
        "shop_chief","shop_disable","shop_disable_date",
        "shop_note","county_id","post_id",
         "fax","telno"] 



class SHOP_QModelForm(ModelForm):

    shop_disable_sdate = forms.DateField(label="停業日期起")
    shop_disable_edate = forms.DateField(label="停業日期迄")

    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["shop_disable_sdate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields["shop_disable_edate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields["post_id"].queryset= Area.objects.none()
        if "county_id" in self.data:
            try:
                county_id = self.data.get("county_id")
                self.fields["post_id"].queryset= Area.objects.filter(county_id=county_id)
            except:
                pass
        elif self.instance.pk:
            self.fields["post_id"].queryset= self.instance.county_id.area_set.all()        

    class Meta :
        model=SHOP
        fields = ["cpnyid","shop_id","shop_name",
        "shop_scname","shop_kind","shopgroup_id",
        "shop_chief","shop_disable","shop_disable_sdate",
        "shop_disable_edate",
        "shop_note","county_id","post_id",
         "fax","telno"] 


class SHOP_RModelForm(ModelForm):
    

    class Meta :
        model=SHOP
        fields = ["shop_id","shop_name","cpnyid",
        "shop_kind","shop_chief"] 

        # fields =[f.name for f in model._meta.get_fields()]  
