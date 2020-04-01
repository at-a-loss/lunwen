from django.db import models

from userapp.models import Users

# Create your models here.
class Title(models.Model):
    title=models.CharField(max_length=20)
    class Meta:
        db_table = "title"

class Attendance(models.Model):
    title=models.ForeignKey("Title",on_delete=models.CASCADE)
    user_id=models.ForeignKey(Users,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "attendance"


