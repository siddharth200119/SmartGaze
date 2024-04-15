from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
# Register your models here.
class Mirror_UsersAdmin (admin.ModelAdmin):
    list_display = ['id','uid', 'face_pattern', 'api_key']

class To_do_listAdmin (admin.ModelAdmin):
    list_display = ['uid','tid','title','item_description','due_date']


class MirrorAdmin (admin.ModelAdmin):
    list_display = ['mid']


admin.site.register(User)
admin.site.register(Mirror_Users, Mirror_UsersAdmin)
admin.site.register(To_do_list, To_do_listAdmin)
admin.site.register(Mirror, MirrorAdmin)
