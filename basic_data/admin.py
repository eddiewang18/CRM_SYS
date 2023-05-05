from django.contrib import admin
from .models import CRM_COMPANY,SHOPGROUP,County,Area,SHOP
# Register your models here.

class CRM_COMPANYModelAdmin(admin.ModelAdmin):
    list_display = ['cpnyid','cocname','coename','coscname','cosename','cuser','cdate','ctime','muser','mdate','mtime']


admin.site.register(CRM_COMPANY,CRM_COMPANYModelAdmin)


class SHOPGROUPModelAdmin(admin.ModelAdmin):
    list_display = ['shopgroup_id','shopgroup_name','cuser','cdate','ctime','muser','mdate','mtime']


admin.site.register(SHOPGROUP,SHOPGROUPModelAdmin)

class CountyModelAdmin(admin.ModelAdmin):
    list_display = ['county_id','county_name']


admin.site.register(County,CountyModelAdmin)

class AreaModelAdmin(admin.ModelAdmin):
    list_display = ['county_id','post_id','post_name','postal']


admin.site.register(Area,AreaModelAdmin)


class SHOPModelAdmin(admin.ModelAdmin):
    list_display = ['cpnyid','shop_id','shop_name','shop_scname','shop_kind','shopgroup_id','shop_disable','county_id','post_id']


admin.site.register(SHOP,SHOPModelAdmin)