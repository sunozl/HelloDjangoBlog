import markdown
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import strip_tags
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    '''分类'''
    # 只有一个属性,分类名:django,python
    # 分类和文章属于一对多关系,一个分类可以有很多文章,一个文章只有一个分类
    name = models.CharField('分类名', max_length=100)
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    '''标签'''
    # 只有一个属性,标签名:django学习,python学习
    # 一个标签可以有多个文章,一个文章可以有多个标签,属于多对多关系
    name = models.CharField('标签名', max_length=100)
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name

class Post(models.Model):
    '''文章'''
    # 文章标题
    # admin后台界面,传入位置参数,若不写,则根据field(字段)自动生成
    title = models.CharField('标题', max_length=30)
    # 文章正文
    body = models.TextField('正文') # 不限制长度
    # 文章创建时间和最后一次修改时间
    create_time = models.DateTimeField('创建时间', default=timezone.now())
    modified_time = models.DateTimeField('修改时间')
    # 文章摘要 可以为空,故blank=True
    excerpt =  models.CharField('摘要', max_length=20, blank=True)
    # 分类和文章属于一对多关系
    # 分类被删则属于该分类的文章自动删除,故有on_delete属性,CASCADE是级联删除
    # 因外键和多对多第一个参数必须传入其关联的model,故传入关键字参数
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    # 标签和文章属于多对多关系,标签可以为空
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    # 作者和文章属于一对多关系,故用ForeignKey(外键)
    # User是django内置的用户模型
    # django.contrib.auth是django内置的应用,用来处理网站用户的注册登录等
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    
    # admin后台显示中文
    class Meta:
        verbose_name = '文章'
        # 中文没有复数形式,故等于单数
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
    
    def __str__(self):
        return self.title
        
    # 每次修改文章 修改时间都要设定当前时间
    # 若在字段那里设置default属性,则只会保存第一次默认值,第二次因有值,则不会保存
    def save(self, *args, **kwargs):
        # 把当前类的修改时间设定为当前时间
        # 调用父类(继承的models类)的save方法,写入数据库
        self.modified_time = timezone.now()
        # 由于摘要不需要生成文章目录,所以去掉toc(目录扩展)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # 先将markdown文本渲染成html文本
        # strip_tags 去掉html文本的全部html标签
        # 从文本中取54个字符赋值给 excerpt(摘要)
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)
    
    # 获取文章的id
    # blog:detail 意思是blog应用下的name=detail的函数
    # reverse会解析这个视图函数对应的url,pk=id,这样就获取到每篇文章的id和url了
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
