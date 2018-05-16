from django.db import models
from django.contrib.auth.models import User  # 内置应用，专门用于处理网站用户的注册、登录等流程
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils import timezone
import markdown

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
#from login.models import UserProfile

# Create your models here.
@python_2_unicode_compatible
class Category(models.Model):
    # https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    name = models.CharField(max_length=100,verbose_name="类别名称")  # 超过这个长度的分类名就不能被存入数据库

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "类别"
        verbose_name_plural = verbose_name


# 显示中文：在Python 3 上，因为所有的字段都原生被认为是Unicode，只需使用__str__() 方法（__unicode__() 方法被废弃）。
# 如果你想与Python 2 兼容，你可以使用python_2_unicode_compatible() 装饰你的模型类
@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=50,verbose_name="标签名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=100,verbose_name="标题")
    # body = models.TextField()
    #body = RichTextField()
    body = RichTextUploadingField()
    created_time = models.DateTimeField(default=timezone.now,verbose_name="创建时间")
    modified_time = models.DateTimeField(default=timezone.now,verbose_name="修改时间")  #
    excerpt = models.CharField(max_length=200, blank=True)  # 允许为空
    # 当分类与标签非常多时，分开存储更省空间---sql不能有信息冗余
    category = models.ForeignKey(Category,verbose_name="类别")  # 分类唯一，一对多
    tags = models.ManyToManyField(Tag, blank=True,verbose_name="标签")  # 标签不唯一，也可以为空
    user = models.ForeignKey(User,verbose_name="用户名")

    views = models.PositiveIntegerField(default=0)

    # class Meta:
    #     ordering = ('-created_time')
    def increase_view(self):
        self.views += 1
        self.save(update_fields=['views'])  # 调用 save 方法将更改后的值保存到数据库

    def __str__(self):  # 支持中文，str不能显示中文，应该一样了  3.x??????
        return self.title

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 自动生成摘要：截取文章前几个字符
    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(
                entensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',  # 语法高亮拓展
                ]
            )
            self.excerpt = strip_tags(md.convert(self.body))[:80]
        super(Post, self).save(*args, **kwargs)
        return self.excerpt
