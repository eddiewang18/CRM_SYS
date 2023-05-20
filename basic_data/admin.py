from django.contrib import admin
from .models import (CRM_COMPANY,SHOPGROUP,County,Area,SHOP,CRM_HRUSER,HRUSER_GROUP,
VIPINFO)
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


class HRUSER_GROUPModelAdmin(admin.ModelAdmin):
    list_display = ['group_id','group_name']


admin.site.register(HRUSER_GROUP,HRUSER_GROUPModelAdmin)



class CRM_HRUSERModelAdmin(admin.ModelAdmin):
    list_display = ['cpnyid',"shop_id",'empid','cname','birthday','sex','pwd','county_id','county_id','post_id']


admin.site.register(CRM_HRUSER,CRM_HRUSERModelAdmin)


class VIPINFOModelAdmin(admin.ModelAdmin):
    list_display = ['vip_id',"vip_name",'cpnyid','shop_id','vipinfo_group_id','county_id','post_id','black','birthday','email']


admin.site.register(VIPINFO,VIPINFOModelAdmin)