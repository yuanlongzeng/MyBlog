from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# class UserProfile(AbstractUser):
#     nick_name = models.CharField(max_length=50,default="",null=False,blank=False,verbose_name="昵称")
#     birth = models.DateField(null=True,blank=True,verbose_name="生日")
#     gender = models.CharField(max_length=10,choices=(("male","男"),("female","女")),default="male",verbose_name="性别")
#     address = models.CharField(max_length=100,default="")
#     mobile = models.CharField(max_length=11,null=True,blank=True)
#     image = models.ImageField(upload_to="profile_photo/%Y/%m",default="profile_photo/default.jpg")
#
#     class Meta:
#         verbose_name = "用户信息"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.username