import markdown
import re
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


from .models import Post, Category, Tag


# Create your views here.
# 接收用户的http请求,处理请求,返回响应
# request是django为我们封装好的http请求
# HttpResponse是封装好的http响应
def index(request):
    # render函数根据我们传入的参数构造HttpResponse
    # 首选把http请求传入,第二个参数找到模板文件,
    # 第三个参数把模板变量的值替换成上下文字典(context)中的值
    # 最后,模板中的内容传递给HttpResponse对象并返回给浏览器
    # (render函数隐式的完成这个过程)
    # 用户的浏览器显示出我们编写的html内容
    post_list = Post.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', context={
        # 'title': '我的博客首页',
        # 'welcom': '欢迎访问我的博客首页'
        'post_list': post_list
    })
    
def detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    # 让文章支持markdown语法(非常简单,强烈建议学习一下)
    # pip install markdown 在虚拟环境下安装python markdown
    # 这个第三方库是将markdown格式的文本解析成标准的HTML文档
    # 导入markdown 在模板文件中使用safe过滤器,表示这是安全的html文档
    md = markdown.Markdown(# 额外的参数,对markdown语法的扩展
                            extensions=[
                                # 基础扩展
                                'markdown.extensions.extra',
                                # 高亮扩展
                                'markdown.extensions.codehilite',
                                # 自动生成目录
                                # 'markdown.extensions.toc',
                                # 引入TocExtension toc变成TocExtension实例
                                # slugify参数可以接收一个函数
                                # 导入的slugify函数可以处理中文标题的锚点值
                                TocExtension(slugify=slugify),
                            ])
    # 使用convert方法将markdown文档转换成html文档
    post.body = md.convert(post.body)
    # md.toc的属性就是目录(一级到六级标题)的值
    # 将目录的值赋值给post.toc post实例本身没有toc属性 我们动态添加的
    # post.toc = md.toc
    
    # 正则表达式去匹配模板中 ul标签中的内容,如果不为空,说明有目录,则提取ul中的值
    # 赋值给post.toc,否则设置为空字符串
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc,
        re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'post': post})
    
def archive(request, year, month):
    '''归档 显示某一日期的所有文章'''
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month,
                                    )
    return render(request, 'blog/index.html', 
                  context={'post_list': post_list})
                  
def category(request, pk):
    '''分类 显示某一分类的所有文章'''
    cate = get_object_or_404(Category, id=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', 
                  context={'post_list': post_list})
                  
def tag(request, pk):
    '''标签 显示某一标签的所有文章'''
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t)
    return render(request, 'blog/index.html', 
                  context={'post_list': post_list})
