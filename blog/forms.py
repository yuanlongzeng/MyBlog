from django import forms
from .models import Post
#from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    city = [['JS', '江苏'], ['zj', '浙江'], ['tj', '天津'], ['bj', '北京']]
    user_name = forms.CharField(label='姓名', max_length=20, initial='您的姓名')  # initial为默认值
    user_city = forms.ChoiceField(label='城市', choices=city)
    user_school = forms.BooleanField(label='是否在校生', required=False)  # 不一定在校，所以不要求一定勾选
    user_email = forms.EmailField(label='电子邮件')  # 能够验证email格式
    user_msg = forms.CharField(label='意见', widget=forms.Textarea)


class PostForm(forms.ModelForm):
    #captcha = CaptchaField()  # 验证码也是统一在form.is_valid()验证的，竟然会自动设置位置？？

    class Meta:
        model = Post  # 窗体引用的model
        fields = ['category', 'title', 'body', 'views']  # 使用的字段

    def __init__(self, *args, **kwargs):  # label变成中文名
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = '类别'
        self.fields['title'].label = '标题'
        self.fields['body'].label = '内容'
        self.fields['views'].label = '阅览量'
        self.fields['captcha'].label = '请输入验证码'


class UploadForm(forms.Form):
    file = forms.FileField()
