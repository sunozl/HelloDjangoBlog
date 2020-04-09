# 自定义模板标签三部曲

from django import template # 1.导入template模块
from ..forms import CommentForm

register = template.Library() # 2.实例Library类

# 3.装饰为自定义模板标签
@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True) 
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm
    return {
        'form': form,
        'post': post,
    }
    
@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    # 获取这篇文章对应的所有评论(评论的外键是文章/多对一关系) 
    # 关联的外键都有 xxx.set属性
    # xxx_set.all() 相等于 Comment.objects.filter(post=post)
    comment_list = post.comment_set.all()
    comment_count = comment_list.count()
    return {
        'comment_list': comment_list,
        'comment_count': comment_count,
    }


