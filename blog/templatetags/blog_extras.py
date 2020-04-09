from django import template

from ..models import Post, Category, Tag

register = template.Library()

# 装饰器,告诉django,这个函数是我们自定义的一个类型为inclusion_tag的模板标签 
# 第二个参数为True,代表渲染第一个参数的模板时,不仅传入字典值
# 还会传入父模板(即使用自定义标签的模板)的上下文(渲染父模板的视图函数中的context)
@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
# 该模板标签和视图函数的功能类似,返回一个字典值,字典的值作为模板变量内容
# 传入装饰器的第一个参数指定的模板
def show_recent_posts(context, num=5):
    '''最新文章标签'''
    return {
        'recent_post_list': Post.objects.all()[:num]
    }
    
@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    '''归档标签'''
    return {
        # dates方法返回一个列表,列表中的元素为每一篇文章的创建时间,是date对象
        # 精确的月份,降序排列 一一对应这三个参数
        'date_list': Post.objects.dates('create_time', 'month', order='DESC')
    }

@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    '''分类标签'''
    return {
        'category_list': Category.objects.all(),
    }

@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    '''标签云标签'''
    return {
        'tag_list': Tag.objects.all()
    }
