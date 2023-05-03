from django.contrib import admin
from .models import CRM_COMPANY,SHOPGROUP
# Register your models here.

class CRM_COMPANYModelAdmin(admin.ModelAdmin):
    list_display = ['cpnyid','cocname','coename','coscname','cosename','cuser','cdate','ctime','muser','mdate','mtime']


admin.site.register(CRM_COMPANY,CRM_COMPANYModelAdmin)


class SHOPGROUPModelAdmin(admin.ModelAdmin):
    list_display = ['shopgroup_id','shopgroup_name','cuser','cdate','ctime','muser','mdate','mtime']


admin.site.register(SHOPGROUP,SHOPGROUPModelAdmin)
