from django.contrib import admin
from .models import *
# Register your models here.

class Mirror_UsersAdmin(admin.ModelAdmin):
    list_display = ['id','username','first_name','last_name','face_pattern','spotify_access_token','spotify_refresh_token']
    search_fields = ['id','first_name','last_name','username']

class To_do_listAdmin(admin.ModelAdmin):
    list_display = ['userid','tid','title','item_description','due_date']

class MirrorAdmin(admin.ModelAdmin):
    list_display = ['mid']

class BridgeAdmin(admin.ModelAdmin):
    list_display = ['userid','mirrorid','layout','alarm_date','alarm_time']

class NewsPrefAdmin(admin.ModelAdmin):
    list_display = ['pid','userid','topic']

class NewsPrefBridgeAdmin(admin.ModelAdmin):
    list_display = ['pid','userid']

admin.site.register(Mirror_Users, Mirror_UsersAdmin)
admin.site.register(To_do_list, To_do_listAdmin)
admin.site.register(Mirror, MirrorAdmin)
admin.site.register(Bridge, BridgeAdmin)
admin.site.register(News_pref, NewsPrefAdmin)
admin.site.register(News_pref_Bridge, NewsPrefBridgeAdmin)