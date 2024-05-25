from django.db import models
from django.contrib.auth.models import AbstractUser


class Mirror_Users(AbstractUser):       
    face_pattern = models.CharField(max_length=5000)
    # api_key = models.CharField(max_length=300)
    spotify_access_token = models.CharField(max_length=350, null=True, blank=True)
    spotify_refresh_token = models.CharField(max_length=350, null=True, blank=True)


    class Meta:
        verbose_name = 'Mirror User'
        verbose_name_plural = 'Mirror Users'
        db_table = 'Users'
        # managed = False


    def __str__(self):
        return str(self.id)
    

class Mirror(models.Model):
    mid = models.AutoField(primary_key=True)
    mirror_name = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'Mirrors'
        # managed = False

    def __str__(self):
        # return str(self.mid)
        return f"{self.mid}: {self.mirror_name}"
    
    
class To_do_list(models.Model):

    status_choices = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ]

    tid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    item_description = models.CharField(max_length=500)  
    due_date = models.DateTimeField(auto_now=False)
    task_status = models.CharField(max_length=20, choices=status_choices, default='Pending')
    userid = models.ForeignKey(Mirror_Users, verbose_name='User ID', on_delete=models.CASCADE, related_name='todo_list')

    class Meta:
        verbose_name = 'ToDo List'
        db_table = 'To_do_list'
        # managed = False

    def __str__(self):
        return f"{self.tid} : {self.title} "


class Bridge(models.Model):
    userid = models.ForeignKey(Mirror_Users, verbose_name='User ID', on_delete=models.CASCADE,  related_name='alarm_users')
    mirrorid = models.ForeignKey(Mirror, verbose_name='Mirror ID', on_delete=models.CASCADE,  related_name='alarm_mirror')
    layout = models.CharField(null=True, blank=True, max_length=50)
    alarm_time = models.TimeField(null=True, blank=True)
    alarm_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'User Mirror Bridge'
        db_table = 'User_mirror_bridge'



class News_pref(models.Model):
    pid = models.AutoField(primary_key=True, verbose_name = 'Topic ID')
    topic = models.CharField(null=True, blank=True, max_length=300)
    userid = models.ForeignKey(Mirror_Users, verbose_name='User ID', on_delete=models.CASCADE,  related_name='news_users')


    class Meta:
        verbose_name = 'News Preference'
        db_table = 'news_pref'

    def __str__(self):
        return str(self.pid)



class News_pref_Bridge(models.Model):
    pid = models.ForeignKey(News_pref, verbose_name='Topic ID', on_delete=models.CASCADE)
    userid = models.ForeignKey(Mirror_Users, verbose_name='User ID', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'News Preference Bridge'
        db_table = 'news_pref_bridge'

    def __str__(self):
        return f"{self.pid} - {self.userid}"