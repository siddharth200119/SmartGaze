from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

#Users of the Mirror
class Mirror_Users(AbstractUser):       
    uid = models.IntegerField(null=True, verbose_name='User_ID', blank=True)
    face_pattern = models.CharField(max_length=2000, null=True, blank=True)
    api_key = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        verbose_name = 'Mirror User'
        verbose_name_plural = 'Mirror Users'
        # db_table = 'Mirror_Users'
        # managed = False

    def _str_(self):
        return str(self.uid)

    
# Model of the Mirror
class Mirror(models.Model):
    mid = models.IntegerField(null=True, blank=True)

    # class Meta:
    #     db_table = 'Mirrors'
    #     managed = True

# Model to store the todo list items
class To_do_list(models.Model):
    tid = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=50)
    item_description = models.CharField(max_length=500)  
    due_date = models.DateTimeField(auto_now=False)
    uid = models.ForeignKey(Mirror_Users, verbose_name='User_ID', on_delete=models.CASCADE,  related_name='todo_list', null=True, blank=True)

    class Meta:
        verbose_name = 'To Do List'
        verbose_name_plural = 'To Do Lists'
        # db_table = 'To_do_list'
        # managed = True  

    def _str_(self):
        return f"{self.tid}: {self.title} by {self.uid}"