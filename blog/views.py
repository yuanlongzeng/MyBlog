from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, Http404, JsonResponse  # raise Http404('找不到相关内容。')
from .models import Post, Category, Tag
import markdown, pygments
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
# from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from . import forms
import os
from django.conf import settings
import uuid


# Create your views here.
def index(req):
    # return HttpResponse('<h1>欢迎来到我的博客！</h1>')
    post_list = Post.objects.all().order_by('created_time')
    return render(req, 'blog/index.html', context={'post_list': post_list})


def detail(req, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        post.increase_view()
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',  # 语法高亮拓展
                                          'markdown.extensions.toc',  # 自动生成目录
                                      ])
        return render(req, 'blog/detail.html', context={'post': post})
    except:
        return redirect('/')  # 以post/没有相关文章时就跳转到首页  内置视图中怎么用？？？


def archives(req, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(req, 'blog/index.html', context={'post_list': post_list})


def category(req, pk):
    cate = get_object_or_404(Category, pk=pk)  # 分类的 id 值
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(req, 'blog/index.html', context={'post_list': post_list})


def search(req):
    q = req.GET.get('q')
    err_msg = ''

    if not q:
        err_msg = '请输入关键词。'
        return render(req, 'blog/index.html', {'error_msg': err_msg})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(req, 'blog/index.html', {'error_msg': err_msg, 'post_list': post_list})


#@csrf_exempt  使用{%csrf_token%}
def contact(req):
    if req.method == 'POST':
        form = forms.ContactForm(req.POST)
        # fileform = forms.UploadForm(req.POST, req.FILES)
        # # 在此之前先判断是否是否有上传：
        #
        #
        # if fileform.is_valid():
        #     file = req.FILES['file']  # 得到的也是二进制文件流
        #     if 'get_file' in req.POST:
        #         save_static_dir(file, 'jpg')
        #         #return HttpResponse('上传成功')
        #         msg = '上传成功'
        # else:  # 使用默认文件
        #         save_static_dir('没有文件', 'txt')

        if form.is_valid():
            msg = {'msg': '感谢您的反馈'}
            user_name = form.cleaned_data['user_name']  # req.POST.get('user_name')
            user_city = form.cleaned_data['user_city']
            user_school = form.cleaned_data['user_school']
            user_email = form.cleaned_data['user_email']
            user_msg = form.cleaned_data['user_msg']
            # 可以存入数据库中
            save_static_dir(user_city + " " + user_email + " " + user_msg + " " + user_name + " " + str(user_school),
                            'txt')
            # msg = '感谢你的反馈,来自于httpresponse'
            # return HttpResponse(msg)  # ajax刷新返回信息  直接返回字符串内容

            msg = {'msg': '感谢你的反馈。'}
            return JsonResponse(msg)  # 列表也可以这样传
        else:
            # msg = '请重新输入。'
            msg = {'msg': '请重新输入'}
            # return HttpResponse(msg)  # ajax刷新返回信息  直接返回字符串内容
            return JsonResponse(msg)  # 列表也可以这样传
    else:
        a = req.GET.get('msg')
        if a is None:
            form = forms.ContactForm()
            # fileform = forms.UploadForm()
            msg = '请填写'

            return render(req, 'blog/contact.html', locals())


def save_static_dir(file, file_type):
    import datetime
    target = os.path.join(settings.BASE_DIR, 'static', str(uuid.uuid4()) + '.' + file_type)
    if not isinstance(file, str):
        with open(target, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
    else:
        target = os.path.join(settings.BASE_DIR, 'static', '反馈' + '.' + file_type)
        with open(target, 'a',
                  encoding='utf-8') as f:  # 在Win上可以，使用的是默认编码GBK，但是ubuntu的默认编码不支持中文  sys.stdout.encoding--ANSI
            f.write(file + " " + str(datetime.datetime.now()) + '\n')
    return os.path.basename(target)


def postMF(req):
    post_form = forms.PostForm()
    models = Post.objects.all()
    if req.session.test_cookie_worked():  # 测试是否支持Cookie
        req.session.delete_test_cookie()
        msg = '有该浏览器的Cookie'
    else:
        msg = '不曾访问'
    req.session.set_test_cookie()
    return render(req, 'blog/post.html', locals())


# 类视图
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'  # 所得数据会被传递给模板
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 2


class CategoryView(IndexView):
    # 属性值继承IndexView的
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))  # 在类视图中，从 URL 捕获的命名组参数值保存在实例的 kwargs 属性
        # 覆写了父类的 get_queryset 方法
        return super(CategoryView, self).get_queryset().filter(category=cate)


class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year,
                                                              created_time__month=month
                                                              )


# ????
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        res = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_view()
        return res  # 视图必须返回一个 HttpResponse 对象

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            TocExtension(slugify=slugify),  # 处理标题的锚点值,slugify可以处理中文
        ])
        post.body = md.convert(post.body)  # 将Markdown 文本渲染成 HTML
        post.toc = md.toc  # 动态添加了 toc 属性
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        return context


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


def handler404(req):
    # return HttpResponse("HHHHHH")
    return render_to_response('404.html')
