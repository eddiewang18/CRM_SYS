from .models import CRM_COMPANY,SHOPGROUP
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError


class CRM_COMPANY_ModelForm(ModelForm):
    
    class Meta :
        model=CRM_COMPANY
        fields = ["cpnyid","cocname","coename","coscname","cosename"]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.errList = []
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