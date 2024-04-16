from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# class MirrorUserManager(BaseUserManager):
#     def get_by_natural_key(self, uid):
#         return self.get(uid=uid)

class Mirror_Users(AbstractUser):       
    face_pattern = models.CharField(max_length=2000)
    api_key = models.CharField(max_length=300)

    class Meta:
        verbose_name = 'Mirror User'
        verbose_name_plural = 'Mirror Users'
        db_table = 'Users'
        # managed = False


    def __str__(self):
        return str(self.id)
    

class Mirror(models.Model):
    mid = models.IntegerField()

    class Meta:
        db_table = 'Mirrors'
        # managed = False


class To_do_list(models.Model):
    tid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    item_description = models.CharField(max_length=500)  
    due_date = models.DateTimeField(auto_now=False)
    complete = models.BooleanField(default=False)  # Default to False for pending
    userid = models.ForeignKey(Mirror_Users, verbose_name='User_ID', on_delete=models.CASCADE,  related_name='todo_list')

    class Meta:
        verbose_name = 'ToDo List'
        db_table = 'To_do_list'
        # managed = False

    def __str__(self):
        return f"{self.tid}: {self.title} by {self.userid}"


class Alarm(models.Model):
    userid = models.ForeignKey(Mirror_Users, verbose_name='User_ID', on_delete=models.CASCADE,  related_name='alarm_users')
    mid = models.ForeignKey(Mirror, verbose_name='Mirror_ID', on_delete=models.CASCADE,  related_name='alarm_mirror')
    layout = models.CharField(null=True, blank=True, max_length=50)
    alarm_time = models.TimeField(null=True, blank=True)
    alarm_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'User Alarm'
        db_table = 'User_mirror_bridge'