from .models import (
    VIP_LABEL_GROUP,
    VIP_LABEL
)

from basic_data.forms import (
    set_class_attr2_fields,clean_fieldName_id,
    clean_fieldName
    )
from django.forms import ModelForm 
from django import forms

class ColorField(forms.CharField):
    widget = forms.TextInput(attrs={'type': 'color'})

class VIP_LABEL_GROUP_ModelForm(ModelForm):
    color = ColorField()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        set_class_attr2_fields(self.fields,'form_field',{"label_gid":{"class":"pkField"}})
        self.errList = []
        self.verbose_name_fields = []
        self.return_query_cols = []
        for i in VIP_LABEL_GROUP._meta.get_fields(): 
            try:
                self.verbose_name_fields.append(i.verbose_name)
                self.return_query_cols.append(i.name)
            except:
                continue
    class Meta :
        model = VIP_LABEL_GROUP
        fields = [
            "cpnyid","label_gid","label_gname","formula_id","color",
            "label_enable","xor","descr"
        ]
    
    def clean_label_gid(self):
        return clean_fieldName_id(self,"label_gid","標籤群組代號",VIP_LABEL_GROUP)

    def clean_shopgroup_name(self):
        return clean_fieldName(self,"label_gid","label_gname","標籤群組名稱",VIP_LABEL_GROUP)


class VIP_LABEL_GROUP_QModelForm(ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        set_class_attr2_fields(self.fields,"qfield")
    class Meta :
        model=VIP_LABEL_GROUP
        fields =  [
            "cpnyid","label_gid","label_gname",
            "label_enable","xor","formula_id"
        ]


class VIP_LABEL_ModelForm(ModelForm):
    class Meta:
        model = VIP_LABEL
        fields = [
            "label_id","label_name","calmin",
            "calmax","label_enable","label_gid"
        ]
    def clean_label_id(self):
        return clean_fieldName_id(self,"label_id","標籤代號",VIP_LABEL)

    def clean_label_name(self):
        return clean_fieldName(self,"label_id","label_name","標籤名稱",VIP_LABEL)
  