from .models import CRM_COMPANY,SHOPGROUP,SHOP,Area
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

def set_class_attr2_fields(fields:dict,general_attrs:str,specific_fields_attrs=None):
    """
    這個函數用來為表單的欄位添加屬性
    fields > 為表單畫面上的欄位，通常用ModelForm的屬性fields
    general_attrs > 以字串型態來表現哪些屬性是表單畫面上欄位共同擁有的
    specific_fields_cls_attrs > 預設值為None，若有值，則為字典包字典的型態 => {field_name1:{attr_name1:attr_value1},....}
                                第一層字典的key為畫面上的欄位名稱，值為字典(屬姓名對屬性值)
                                可以將要額外設置給某欄位的某一屬性的資料設置在此參數中    
                                """
    for name,field in fields.items():
        field.widget.attrs['class'] = general_attrs
        if specific_fields_attrs is not None:
            if name in specific_fields_attrs:
                attrs_dict = specific_fields_attrs[name]
                for k,v in attrs_dict.items():
                    if k not in field.widget.attrs:
                        field.widget.attrs[k] = v 
                    else:
                        field.widget.attrs[k] +=" "+v 



class CRM_COMPANY_ModelForm(ModelForm):
    # verbose_name_fields = []
    # return_query_cols = []
    # for i in CRM_COMPANY._meta.get_fields(): 
    #     try:
    #         verbose_name_fields.append(i.verbose_name)
    #         return_query_cols.append(i.name)
    #     except:
    #         continue
    class Meta :
        model=CRM_COMPANY
        fields = ["cpnyid","cocname","coename","coscname","cosename"]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.errList = []
        set_class_attr2_fields(self.fields,'form_field',{"cpnyid":{"class":"pkField"}})
        self.verbose_name_fields = []
        self.return_query_cols = []
        for i in CRM_COMPANY._meta.get_fields(): 
            try:
                self.verbose_name_fields.append(i.verbose_name)
                self.return_query_cols.append(i.name)
            except:
                continue

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
        
class CRM_COMPANY_QModelForm(ModelForm):
    class Meta :
        model = CRM_COMPANY
        fields = ["cpnyid","cocname","coename","coscname","cosename"]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        set_class_attr2_fields(self.fields,"qfield",specific_fields_attrs=None)



class SHOPGROUP_ModelForm(ModelForm):
    class Meta :
        model=SHOPGROUP
        fields = ["shopgroup_id","shopgroup_name"]



class SHOP_ModelForm(ModelForm):
    # verbose_name_fields = []
    # return_query_cols = []
    # for i in SHOP._meta.get_fields(): 
    #     try:
    #         verbose_name_fields.append(i.verbose_name)
    #         return_query_cols.append(i.name)
    #     except:
    #         continue

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["shop_disable_date"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )

        set_class_attr2_fields(self.fields,'form_field',{"shop_disable_date":{"disabled":"true"},"shop_id":{"class":"pkField"}})
        self.errList = []

        self.fields["post_id"].queryset= Area.objects.none()
        if "county_id" in self.data:
            try:
                county_id = self.data.get("county_id")
                self.fields["post_id"].queryset= Area.objects.filter(county_id=county_id)
            except:
                pass
        elif self.instance.pk:
            self.fields["post_id"].queryset= self.instance.county_id.area_set.all()        

        self.verbose_name_fields = []
        self.return_query_cols = []
        for i in SHOP._meta.get_fields(): 
            try:
                self.verbose_name_fields.append(i.verbose_name)
                self.return_query_cols.append(i.name)
            except:
                continue

    class Meta :
        model=SHOP
        fields = ["cpnyid","shop_id","shop_name",
        "shop_scname","shop_kind","shopgroup_id",
        "shop_chief","shop_disable","shop_disable_date",
        "shop_note","county_id","post_id",
         "fax","telno"] 

    def clean_shop_id(self):
        shop_id = self.cleaned_data.get("shop_id")
        data_exists = None
        if not self.instance.pk :
            data_exists = SHOP.objects.filter(shop_id=shop_id).exists()
        else:
            data_exists = SHOP.objects.filter(shop_id=shop_id).exclude(shop_id=shop_id).exists()
        if data_exists :
            errMsg = f"分店編號 {shop_id} 已存在 不可重複輸入"
            self.errList.append(errMsg)
            raise ValidationError(errMsg)
        else:
            return shop_id


    
    def clean_shop_name(self):
        shop_name = self.cleaned_data.get("shop_name")
        shop_id = self.cleaned_data.get("shop_id")
        data_exists = None
        if not self.instance.pk :
            data_exists = SHOP.objects.filter(shop_name=shop_name).exists()
        else:
            data_exists = SHOP.objects.filter(shop_name=shop_name).exclude(shop_id=shop_id).exists()


        if data_exists :
            errMsg = f"分店名稱 {shop_name} 已存在 不可重複輸入"
            self.errList.append(errMsg)

            raise ValidationError(errMsg)
        else:
            return shop_name 



class SHOP_QModelForm(ModelForm):

    shop_disable_date_sdate = forms.DateField(label="停業日期起")
    shop_disable_date_edate = forms.DateField(label="停業日期迄")

    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["shop_disable_date_sdate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields["shop_disable_date_edate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        set_class_attr2_fields(self.fields,"qfield",specific_fields_attrs={"shop_disable_date_sdate":{"disabled":"true"},"shop_disable_date_edate":{"disabled":"true"}})

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
        "shop_chief","shop_disable","shop_disable_date_sdate",
        "shop_disable_date_edate",
        "shop_note","county_id","post_id",
         "fax","telno"] 


class SHOP_RModelForm(ModelForm):
    

    class Meta :
        model=SHOP
        fields = ["shop_id","shop_name","cpnyid",
        "shop_kind","shop_chief"] 

        # fields =[f.name for f in model._meta.get_fields()]  
