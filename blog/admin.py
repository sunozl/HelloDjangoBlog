from django.contrib import admin
from .models import Post, Category, Tag

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    # 后台列表显示
    list_display = ['title', 'create_time', 'modified_time', 'category',
        'author']
    # 添加文章表单
    fields = ['title', 'body', 'excerpt', 'category', 'tags']
    
    # 第三个参数是关联对象的实例(Post的实例)
    def save_model(self, request, obj, form, change):
        # 请求对象的user属性就是登录名
        obj.author = request.user
        super().save_model(request, obj, form, change)

# PostAdmin和Post关联
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
