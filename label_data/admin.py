from django.contrib import admin
from .models import (
    VIP_LABEL_GROUP,
    VIP_LABEL
)
# Register your models here.
class VIP_LABEL_GROUPModelAdmin(admin.ModelAdmin):
    list_display = ['cpnyid','label_gid','label_gname','formula_id','descr','color',"xor",'label_enable','cuser','cdate','ctime','muser','mdate','mtime']


admin.site.register(VIP_LABEL_GROUP,VIP_LABEL_GROUPModelAdmin)


class VIP_LABELModelAdmin(admin.ModelAdmin):
    list_display = ['label_gid','label_id','label_name','calmin','calmax','label_enable','cuser','cdate','ctime','muser','mdate','mtime']


admin.site.register(VIP_LABEL,VIP_LABELModelAdmin)