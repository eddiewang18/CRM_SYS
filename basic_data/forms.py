from .models import (
    CRM_COMPANY,SHOPGROUP,SHOP,Area,HRUSER_GROUP,
    CRM_HRUSER,VIPINFO_GROUP,VIPINFO,ProductType,
    Product
)
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from datetime import date
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

def clean_fieldName_id(this,fieldName_id:str,fieldName_id_cname,model):
    """
    檢核表單中的資料的編號(primary key)是否有重複寫入
    this > ModelForm物件
    fieldName_id > table中編號的欄位名稱
    fieldName_id_cname >table中編號對應的中文名稱
    
    """
    fieldName_id_val = this.cleaned_data.get(fieldName_id)
    data_exists = None
    if not this.instance.pk :
        data_exists = model.objects.filter(**{fieldName_id:fieldName_id_val}).exists()
    else:
        data_exists = model.objects.filter(**{fieldName_id:fieldName_id_val}).exclude(**{fieldName_id:fieldName_id_val}).exists()
    if data_exists :
        errMsg = f"{fieldName_id_cname} {fieldName_id_val} 已存在 不可重複輸入"
        this.errList.append(errMsg)
        raise ValidationError(errMsg)
    else:
        return fieldName_id_val

def clean_fieldName(this,fieldName_id,fieldName,fieldName_cname,model):
    """
    檢核表單中的資料的顯示名稱是否有重複寫入
    this > ModelForm物件
    fieldName_id > table中編號的欄位名稱
    fieldName_cname >table中對應顯示的中文名稱
    
    """
    fieldName_val = this.cleaned_data.get(fieldName)
    fieldName_id_val = this.cleaned_data.get(fieldName_id)
    data_exists = None
    if not this.instance.pk :
        data_exists = model.objects.filter(**{fieldName:fieldName_val}).exists()
    else:
        data_exists = model.objects.filter(**{fieldName:fieldName_val}).exclude(**{fieldName_id:fieldName_id_val}).exists()
    print(f'data_exists={data_exists}')

    if data_exists :
        errMsg = f"{fieldName_cname} {fieldName_val} 已存在 不可重複輸入"
        this.errList.append(errMsg)
        raise ValidationError(errMsg)
    else:
        return fieldName_val 

class CRM_COMPANY_ModelForm(ModelForm):

    class Meta :
        model=CRM_COMPANY
        fields = ["cpnyid","cocname","coename","coscname","cosename","cdate"]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.errList = []
        self.fields["cdate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control',
                'value':str(date.today())
                }
            )
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
        return clean_fieldName_id(self,"cpnyid","公司編號",CRM_COMPANY)
        # cpnyid = self.cleaned_data.get("cpnyid")
        # data_exists = None
        # if not self.instance.pk :
        #     data_exists = CRM_COMPANY.objects.filter(cpnyid=cpnyid).exists()
        # else:
        #     data_exists = CRM_COMPANY.objects.filter(cpnyid=cpnyid).exclude(cpnyid=cpnyid).exists()
        # if data_exists :
        #     errMsg = f"公司編號 {cpnyid} 已存在 不可重複輸入"
        #     self.errList.append(errMsg)
        #     raise ValidationError(errMsg)
        # else:
        #     return cpnyid

    def clean_cocname(self):
        return clean_fieldName(self,"cpnyid","cocname","公司中文名稱",CRM_COMPANY)
        # cocname = self.cleaned_data.get("cocname")
        # cpnyid = self.cleaned_data.get("cpnyid")
        # data_exists = None
        # if not self.instance.pk :
        #     data_exists = CRM_COMPANY.objects.filter(cocname=cocname).exists()
        # else:
        #     data_exists = CRM_COMPANY.objects.filter(cocname=cocname).exclude(cpnyid=cpnyid).exists()


        # if data_exists :
        #     errMsg = f"公司中文名稱 {cocname} 已存在 不可重複輸入"
        #     self.errList.append(errMsg)
        #     raise ValidationError(errMsg)
        # else:
        #     return cocname 
        
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
        fields = ["shopgroup_id","shopgroup_name","cpnyid"]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.errList = []
    def clean_shopgroup_id(self):
        return clean_fieldName_id(self,"shopgroup_id","分店群組編號",SHOPGROUP)

    def clean_shopgroup_name(self):
        return clean_fieldName(self,"shopgroup_id","shopgroup_name","分店群組名稱",SHOPGROUP)
  

class SHOPGROUP_QModelForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        set_class_attr2_fields(self.fields,"qfield")
    class Meta :
        model=SHOPGROUP
        fields = ["shopgroup_id","shopgroup_name","cpnyid"]

class SHOP_ModelForm(ModelForm):

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
        return clean_fieldName_id(self,"shop_id","分店編號",SHOP)

    def clean_shop_name(self):
        return clean_fieldName(self,"shop_id","shop_name","分店名稱",SHOP)




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




class HRUSER_GROUP_ModelForm(ModelForm):
    class Meta :
        model=HRUSER_GROUP
        fields = ["group_id","group_name","cpnyid"]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.errList = []
    def clean_group_id(self):
        return clean_fieldName_id(self,"group_id","員工群組編號",HRUSER_GROUP)

    def clean_group_name(self):
        return clean_fieldName(self,"group_id","group_name","員工群組名稱",HRUSER_GROUP)

class HRUSER_GROUP_QModelForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        set_class_attr2_fields(self.fields,"qfield")
    class Meta :
        model=HRUSER_GROUP
        fields =  ["group_id","group_name","cpnyid"]
#####################################################

class CRM_HRUSER_ModelForm(ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["pwd"].widget = forms.widgets.PasswordInput(

            )
        self.fields["birthday"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields["indate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )    

        self.fields["quitdate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        set_class_attr2_fields(self.fields,'form_field',{"empid":{"class":"pkField"}})
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
        self.fields["shop_id"].queryset= SHOP.objects.none()
        if "cpnyid" in self.data:
            try:
                cpnyid = self.data.get("cpnyid")
                self.fields["shop_id"].queryset= SHOP.objects.filter(cpnyid=cpnyid)
            except:
                pass
        elif self.instance.pk:
            self.fields["shop_id"].queryset= self.instance.cpnyid.shop_set.all()   



        self.verbose_name_fields = []
        self.return_query_cols = []
        for i in CRM_HRUSER._meta.get_fields(): 
            try:
                self.verbose_name_fields.append(i.verbose_name)
                self.return_query_cols.append(i.name)
            except:
                continue

    class Meta :
        model=CRM_HRUSER
        fields = ["cpnyid","shop_id","empid","cname","ename","identid","birthday",
        "pwd","telno","mobilno","sex","email","indate","quitdate",
        "group_id","emp_type","county_id","email","post_id","note",
        ] 

    def clean_empid(self):
        return clean_fieldName_id(self,"empid","員工編號",CRM_HRUSER)


class CRM_HRUSER_QModelForm(ModelForm):

    birthday_sdate = forms.DateField(label="出生日期起")
    birthday_edate = forms.DateField(label="出生日期迄")
    indate_sdate = forms.DateField(label="到職日期起")
    indate_edate = forms.DateField(label="到職日期迄")
    quitdate_sdate = forms.DateField(label="離職日期起")
    quitdate_edate = forms.DateField(label="離職日期迄")

    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["birthday_sdate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields["birthday_edate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields["indate_sdate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields["indate_edate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )    

        self.fields["quitdate_sdate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields["quitdate_edate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )       
        set_class_attr2_fields(self.fields,"qfield",specific_fields_attrs={})

        self.fields["post_id"].queryset= Area.objects.none()
        if "county_id" in self.data:
            try:
                county_id = self.data.get("county_id")
                self.fields["post_id"].queryset= Area.objects.filter(county_id=county_id)
            except:
                pass
        elif self.instance.pk:
            self.fields["post_id"].queryset= self.instance.county_id.area_set.all()    

        self.fields["shop_id"].queryset= SHOP.objects.none()
        if "cpnyid" in self.data:
            try:
                cpnyid = self.data.get("shop_id")
                self.fields["shop_id"].queryset= SHOP.objects.filter(cpnyid=cpnyid)
            except:
                pass
        elif self.instance.pk:
            self.fields["shop_id"].queryset= self.instance.cpnyid.shop_set.all()   
       

    class Meta :
        model=CRM_HRUSER
        fields = ["cpnyid","shop_id","empid","cname","ename","identid","birthday_sdate","birthday_edate",
        "pwd","telno","mobilno","sex","email","indate_sdate","indate_edate","quitdate_sdate",
        "quitdate_edate","group_id","emp_type","county_id","email","post_id",
        ] 



class VIPINFO_GROUP_ModelForm(ModelForm):

    class Meta :
        model=VIPINFO_GROUP
        fields = ["vipinfo_group_id","vipinfo_group_name","cpnyid"]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.errList = []
    def clean_vipinfo_group_id(self):
        return clean_fieldName_id(self,"vipinfo_group_id","會員群組編號",VIPINFO_GROUP)

    def clean_vipinfo_group_name(self):
        return clean_fieldName(self,"vipinfo_group_id","vipinfo_group_name","會員群組名稱",VIPINFO_GROUP)


class VIPINFO_GROUP_QModelForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        set_class_attr2_fields(self.fields,"qfield")
    class Meta :
        model=VIPINFO_GROUP
        fields = ["vipinfo_group_id","vipinfo_group_name","cpnyid"]



class VIPINFO_ModelForm(ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["apply_date"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields["birthday"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields["end_date"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )


        set_class_attr2_fields(self.fields,'form_field',{"vip_id":{"class":"pkField"}})
        self.errList = []

        self.fields["post_id"].queryset= Area.objects.none()
        self.fields["shop_id"].queryset= SHOP.objects.none()
        self.fields["vipinfo_group_id"].queryset= SHOP.objects.none()


        if "county_id" in self.data:
            try:
                county_id = self.data.get("county_id")
                self.fields["post_id"].queryset= Area.objects.filter(county_id=county_id)
                
            except:
                pass
        elif self.instance.pk:
            self.fields["post_id"].queryset= self.instance.county_id.area_set.all()        


        if "cpnyid" in self.data:
            try:
                cpnyid = self.data.get("cpnyid")
                self.fields["shop_id"].queryset= SHOP.objects.filter(cpnyid=cpnyid)
                self.fields["vipinfo_group_id"].queryset= VIPINFO_GROUP.objects.filter(cpnyid=cpnyid)
            except:
                pass
        elif self.instance.pk:
            self.fields["shop_id"].queryset= self.instance.cpnyid.shop_set.all()   
            self.fields["vipinfo_group_id"].queryset= self.instance.cpnyid.vipinfo_group_set.all()   


        self.verbose_name_fields = []
        self.return_query_cols = []
        for i in VIPINFO._meta.get_fields(): 
            try:
                self.verbose_name_fields.append(i.verbose_name)
                self.return_query_cols.append(i.name)
            except:
                continue

    class Meta :
        model=VIPINFO
        fields = ["vip_id","vip_name","cpnyid","shop_id","vipinfo_group_id","sex",
        "county_id","post_id","birthday","apply_date","telno","black",
        "edu_lv","email","mobilno","job_cat","vip_cpny","end_date",
        "vip_position","familysize","ispromote","vip_FB","vip_IG","vip_LINE","note"] 

    def clean_vip_id(self):
        return clean_fieldName_id(self,"vip_id","會員編號",VIPINFO)





class VIPINFO_QModelForm(ModelForm):

    apply_date_sdate = forms.DateField(label="申請日期起")
    apply_date_edate = forms.DateField(label="申請日期迄")
    birthday_sdate = forms.DateField(label="出生日期起")
    birthday_edate = forms.DateField(label="出生日期迄")
    end_date_sdate = forms.DateField(label="有效日期起")
    end_date_edate = forms.DateField(label="有效日期迄")
    familysize_lowerVal = forms.IntegerField(label="家庭人數下限")
    familysize_upperVal = forms.IntegerField(label="家庭人數上限")

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["apply_date_sdate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields["apply_date_edate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields["birthday_sdate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields["birthday_edate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields["end_date_sdate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields["end_date_edate"].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )


        set_class_attr2_fields(self.fields,"qfield")

        self.fields["post_id"].queryset= Area.objects.none()
        self.fields["shop_id"].queryset= SHOP.objects.none()

        if "county_id" in self.data:
            try:
                county_id = self.data.get("county_id")
                self.fields["post_id"].queryset= Area.objects.filter(county_id=county_id)
            except:
                pass
        elif self.instance.pk:
            self.fields["post_id"].queryset= self.instance.county_id.area_set.all()    

        if "cpnyid" in self.data:
            try:
                cpnyid = self.data.get("cpnyid")
                self.fields["shop_id"].queryset= SHOP.objects.filter(cpnyid=cpnyid)
            except:
                pass
        elif self.instance.pk:
            self.fields["shop_id"].queryset= self.instance.cpnyid.shop_set.all()          

    class Meta :
        model=VIPINFO
        fields = ["vip_id","vip_name","cpnyid","shop_id","vipinfo_group_id","sex",
        "county_id","post_id","birthday_sdate","birthday_edate","apply_date_sdate","apply_date_edate"
        ,"telno","black",
        "edu_lv","email","mobilno","job_cat","vip_cpny","end_date_sdate","end_date_edate",
        "vip_position","ispromote","familysize_lowerVal","familysize_upperVal","vip_FB","vip_IG","vip_LINE",] 


class ProductType_ModelForm(ModelForm):

    class Meta :
        model=ProductType
        fields = ["prod_type_id","prod_type_name","cpnyid"]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.errList = []
    def clean_prod_type_id(self):
        return clean_fieldName_id(self,"prod_type_id","商品類別編號",ProductType)


class ProductType_QModelForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        set_class_attr2_fields(self.fields,"qfield")
    class Meta :
        model=ProductType
        fields = ["prod_type_id","prod_type_name","cpnyid"]


class Product_ModelForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        set_class_attr2_fields(self.fields,'form_field',{"prod_id":{"class":"pkField"}})
        self.errList = []
        self.fields["prod_type_id"].queryset= ProductType.objects.none()


        if "cpnyid" in self.data:
            try:
                cpnyid = self.data.get("cpnyid")
                self.fields["prod_type_id"].queryset= ProductType.objects.filter(cpnyid=cpnyid)
            except:
                pass
        elif self.instance.pk:
            self.fields["prod_type_id"].queryset= self.instance.cpnyid.producttype_set.all()   


        self.verbose_name_fields = []
        self.return_query_cols = []
        for i in Product._meta.get_fields(): 
            try:
                self.verbose_name_fields.append(i.verbose_name)
                self.return_query_cols.append(i.name)
            except:
                continue

    class Meta :
        model=Product
        fields = ["cpnyid","prod_id","prod_name","prod_type_id",
            "prod_unit","price","cost_price","return_price",
            "fixed_price","emp_price","discount_price",
            "discount_rate","origin","barcode","note"
        ] 

    def clean_prod_id(self):
        return clean_fieldName_id(self,"prod_id","商品編號",Product)


class Product_QModelForm(ModelForm):


    price_lowerVal = forms.IntegerField(label="售價下限")
    price_upperVal = forms.IntegerField(label="售價上限")


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        set_class_attr2_fields(self.fields,"qfield")
        self.fields["prod_type_id"].queryset= ProductType.objects.none()
        if "cpnyid" in self.data:
            try:
                cpnyid = self.data.get("cpnyid")
                self.fields["prod_type_id"].queryset= ProductType.objects.filter(cpnyid=cpnyid)
            except:
                pass
        elif self.instance.pk:
            self.fields["prod_type_id"].queryset= self.instance.cpnyid.producttype_set.all()   


    class Meta :
        model=Product
        fields = ["cpnyid","prod_id","prod_name","prod_type_id",
            "prod_unit","price_lowerVal","price_upperVal","origin","barcode"
        ] 
