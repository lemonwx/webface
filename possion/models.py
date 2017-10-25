from django.db import models
from datetime import datetime

# Create your models here.

class Img(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="possion/%Y/%m", max_length=100)
    add_time = models.DateTimeField(default=datetime.now())


class PossionTask(models.Model):
    pre_img_id = models.IntegerField(null=False, default=0)
    bak_img_id = models.IntegerField(null=False, default=0)
    user_id = models.IntegerField(null=False, default=0)
    tgt_img_path = models.ImageField(upload_to="target/%Y/%m", max_length=100)



