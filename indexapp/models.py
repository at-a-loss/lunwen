from django.db import models

# Create your models here.
class Pic(models.Model):
    title=models.CharField(max_length=30)
    status=models.BooleanField()
    create_time=models.DateTimeField(auto_now_add=True)
    pic=models.FileField(upload_to="pics")
    class Meta:
        db_table="pic"