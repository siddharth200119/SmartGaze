from django.contrib import admin
from .models import *
# Register your models here.

class Mirror_UsersAdmin(admin.ModelAdmin):
    list_display = ['id','username','first_name','last_name','face_pattern','api_key']
    search_fields = ['id','first_name','last_name','username']

class To_do_listAdmin(admin.ModelAdmin):
    list_display = ['userid','tid','title','item_description','due_date']

class MirrorAdmin(admin.ModelAdmin):
    list_display = ['mid']

admin.site.register(Mirror_Users, Mirror_UsersAdmin)
admin.site.register(To_do_list, To_do_listAdmin)
admin.site.register(Mirror, MirrorAdmin)
