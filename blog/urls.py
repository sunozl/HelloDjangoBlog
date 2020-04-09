from django.urls import path
from . import views

# 一个网站的流程是怎么样的?
# 用户请求网站(baidu.com)
# 浏览器把客户的访问意图包装成一个http请求,发给请求网站对应的服务器
# 服务器处理请求,生成一段http响应给浏览器,浏览器解读响应,显示内容.end

# django是一个web框架,它的使命就是接受请求,返回响应
# 它处理上述问题的机制是,通过定义url-编写视图-编写模板来处理
# 用户请求,django去urls.py文件中找,找到对应的网址,调用和它绑定在一起的视图函数

# 区分应用程序,避免有相同的视图函数
app_name = 'blog' 

# 把网址和视图函数写在urlpatterns列表中
urlpatterns = [
    # 第一个参数是网址,正则表达式的语法规则
    # 第二个参数是视图函数
    # 第三个参数是前两个参数的别名,模板文件会用到
    path('', views.index, name='index'),
    
    # 文章详情页
    # 排除域名(127.0.0.1:8000)后,以posts/开头
    # <int:pk>,作用是从用户访问的url里获取匹配到的数字,并传递给detail视图函数
    # 如posts/255/ pk=255 传递给detail(request, pk=255)
    path('posts/<int:pk>/', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    path('categorys/<int:pk>/', views.category, name='category'),
    path('tags/<int:pk>/', views.tag, name='tag'),
]
