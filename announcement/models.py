from django.db import models
from personality.models import User
# Create your models here.

class Announce_type(models.Model):
    type=models.CharField(unique=True,max_length=255)
    fields=models.CharField(unique=True,max_length=255)
class Announcement(models.Model):
    user=models.ForeignKey(User,to_field='phone',on_delete=models.CASCADE)
    type=models.ForeignKey(Announce_type,to_field='type',on_delete=models.CASCADE)
    summary=models.CharField(max_length=255,null=True,default=None)
    text=models.TextField(null=True,default=None)
    in_stock=models.BooleanField()
    price=models.BigIntegerField(null=True,default=None)
