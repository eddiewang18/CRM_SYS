from django.contrib import admin
from .models import (
    VIP_LABEL_GROUP,
    VIP_LABEL,
    Sales00,
    Sale01,
)
# Register your models here.
class VIP_LABEL_GROUPModelAdmin(admin.ModelAdmin):
    list_display = ['cpnyid','label_gid','label_gname','formula_id','descr','color',"xor",'label_enable','cuser','cdate','ctime','muser','mdate','mtime']


admin.site.register(VIP_LABEL_GROUP,VIP_LABEL_GROUPModelAdmin)


class VIP_LABELModelAdmin(admin.ModelAdmin):
    list_display = ['label_gid','label_id','label_name','calmin','calmax','label_enable','cuser','cdate','ctime','muser','mdate','mtime']


admin.site.register(VIP_LABEL,VIP_LABELModelAdmin)


class Sales00ModelAdmin(admin.ModelAdmin):
    list_display = ['sale00_id']


admin.site.register(Sales00,Sales00ModelAdmin)

class Sales01ModelAdmin(admin.ModelAdmin):
    list_display = ['sale01_id']


admin.site.register(Sale01,Sales01ModelAdmin)