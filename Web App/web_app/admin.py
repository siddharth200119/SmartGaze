from django.contrib import admin
from .models import *
# Register your models here.

class Mirror_UsersAdmin(admin.ModelAdmin):
    list_display = ['id','username','first_name','last_name','face_pattern','spotify_access_token','spotify_refresh_token']
    search_fields = ['id','first_name','last_name','username']

class To_do_listAdmin(admin.ModelAdmin):
    list_display = ['userid','tid','title','item_description','due_date']
    raw_id_fields = ('userid',)

class MirrorAdmin(admin.ModelAdmin):
    list_display = ['mid', 'mirror_name']

class BridgeAdmin(admin.ModelAdmin):
    list_display = ['userid','mirrorid','layout','alarm_date','alarm_time']
    raw_id_fields = ('userid','mirrorid')

class NewsPrefAdmin(admin.ModelAdmin):
    list_display = ['pid','userid','topic']
    raw_id_fields = ('userid',)


admin.site.register(Mirror_Users, Mirror_UsersAdmin)
admin.site.register(To_do_list, To_do_listAdmin)
admin.site.register(Mirror, MirrorAdmin)
admin.site.register(Bridge, BridgeAdmin)
admin.site.register(News_pref, NewsPrefAdmin)
