from blog.models import Post
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CommentForm

# Create your views here.
def comment(request, post_pk):
    # 获取被评论的文章,把文章和评论关联起来
    # get.. 这个函数的作用是获取的文章(Post)存在时,则获取;否则返回404页面
    post = get_object_or_404(Post, pk=post_pk)
    # 用户提交(输入)的数据封装在request.POST中,这是一个字典
    # 根据输入的数据实例化一个表单
    form = CommentForm(request.POST)
    
    if form.is_valid():# 检查数据是否有效
        # 根据输入的数据生成表单的实例,但不保存到数据库
        comment = form.save(commit=False)
        # 评论和文章关联
        comment.post = post
        # 保存到数据库
        comment.save()
        
        messages.add_message(request, messages.SUCCESS, '评论发表成功',
                            extra_tags='success')
        # 重定向到post的detail页面
        # redirect 这个函数接受一个模型的实例时,会调用实例的get_absolute_url方法
        # 然后重定向到get_absolute_url方法返回的URL
        return redirect(post)
    # 数据不合法,渲染一个错误表单页面
    # 被评论的文章也传递给模板,提交表单需要post.pk参数
    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, 
        '评论发表失败!请修改表单中的错误后重新提交.', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)
