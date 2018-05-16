from django.contrib.syndication.views import Feed
from .models import Post

class AllPosts(Feed):
    title = 'RSS订阅'
    link = '/' # 通过聚合阅读器跳转到网站的地址
    description = '描述信息'

    def items(self):
        return Post.objects.all()

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.body
