from django.contrib import admin
from .models import Post, Category, Tag

import xadmin
from xadmin import forms, views


# Register your models here.这样可以在后台进行显示、管理
# class PostAdmin(admin.ModelAdmin):
#     list_display = ['title', 'created_time', 'modified_time', 'category', 'user']
#
#
# admin.site.register(Post, PostAdmin)
# admin.site.register(Category)
# admin.site.register(Tag)

class BaseSetting:
    enable_themes = True  # 设置主题
    use_bootswatch = True


class GlobalSetting:
    site_title = "我的博客"  # 设置主题
    site_footer = "ylz's blog"
    menu_style = "accordion"  #每个app下的model可展开-收缩


class PostAdmin:
    list_display = ['title', 'created_time', 'modified_time', 'category', 'user']  # 会展示的表头
    search_fields = ['title', 'category', 'user']  # 符合搜索框
    list_filter = ['title', 'created_time', 'modified_time', 'category', 'user']  # 更详细的搜索


class CategoryAdmin:
    list_display = ['name']  # 会展示的表头
    search_fields = ['name']  # 符合搜索框
    list_filter = ['name']  # 更详细的搜索


class TagAdmin:
    list_display = ['name']  # 会展示的表头
    search_fields = ['name']  # 符合搜索框
    list_filter = ['name']  # 更详细的搜索


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)

xadmin.site.register(Post, PostAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Tag, TagAdmin)
