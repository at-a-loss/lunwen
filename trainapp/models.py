from django.db import models

# Create your models here.
from userapp.models import Dept


class Train(models.Model):
    name=models.CharField(max_length=30)
    # password=models.CharField(max_length=20)
    gender=models.BooleanField()
    phone=models.CharField(max_length=13)
    create_time = models.DateTimeField(auto_now_add=True)
    # addr1=models.CharField(max_length=10)
    addr=models.CharField(max_length=30)
    head = models.FileField(upload_to="heads")
    # freeze=models.BooleanField()
    dept_id=models.ForeignKey(Dept,on_delete=models.CASCADE)
    # performance=models.IntegerField()
    status=models.BooleanField()
    class Meta:
        db_table="train"