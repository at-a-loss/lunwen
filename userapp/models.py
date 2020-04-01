from django.db import models

# Create your models here.
class Users(models.Model):
    name=models.CharField(max_length=30)
    password=models.CharField(max_length=20)
    gender=models.BooleanField()
    phone=models.CharField(max_length=13)
    create_time = models.DateTimeField(auto_now_add=True)
    addr1=models.CharField(max_length=10)
    addr2=models.CharField(max_length=30)
    head = models.FileField(upload_to="heads")
    freeze=models.BooleanField()
    dept_id=models.ForeignKey("Dept",on_delete=models.CASCADE)
    performance=models.IntegerField()
    class Meta:
        db_table="users"

class Dept(models.Model):
    name=models.CharField(max_length=20)
    salary = models.CharField(max_length=10)
    class Meta:
        db_table="dept"