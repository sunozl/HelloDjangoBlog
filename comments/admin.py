from django.contrib import admin
from .models import Comment

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    # 后台列表显示
    list_display = ['name', 'email', 'url', 'post', 'create_time']
    # 添加表单显示
    fields = ['name', 'email', 'url', 'text', 'post']
    
admin.site.register(Comment, CommentAdmin)
