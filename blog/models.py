from django.db import models

# Create your models here.


class MyBaseModel(models.Model):
    is_active = models.BooleanField(default=False, verbose_name='is_active')
    is_download = models.BooleanField(default=False, verbose_name='is_download')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='created_date')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='updated_date')

    class Meta:
        abstract = True
        ordering = ('pk',)

    def __str__(self):
        raise NotImplemented('Implement __str__ method')


class Category(MyBaseModel):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name='category')
    link = models.URLField(default='example.com', verbose_name='link')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Author(MyBaseModel):
    title = models.CharField(max_length=100, null=False, verbose_name='title')
    link = models.URLField(default='example.com', verbose_name='link')

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Tag(MyBaseModel):
    title = models.CharField(max_length=100, null=False, verbose_name='title')
    link = models.URLField(default='example.com', verbose_name='link')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('id',)

    def __str__(self):
        return self.title


class KeyWord(MyBaseModel):
    title = models.CharField(max_length=100, null=False, verbose_name='title')

    class Meta:
        verbose_name = 'Key Word'
        verbose_name_plural = 'Key Words'
        ordering = ('id',)

    def __str__(self):
        return self.title


class KeyWordResult(MyBaseModel):
    keyword = models.ForeignKey(
        KeyWord,
        null=True,
        blank=False,
        on_delete=models.PROTECT,
        verbose_name='Key Word',
    )

    class Meta:
        verbose_name = 'Key Word Result'
        verbose_name_plural = 'Key Word Results'
        ordering = ('id',)

    def __str__(self):
        return str(self.keyword)


class Article(MyBaseModel):
    title = models.CharField(max_length=250, null=False, verbose_name='title')
    description = models.TextField(null=True, blank=False, verbose_name='Description')
    link = models.URLField(null=False, default='example.com', verbose_name='link')
    posted = models.DateTimeField(null=True, blank=True, verbose_name='Posted at ')
    author = models.ForeignKey(
        Author,
        null=True,
        blank=False,
        on_delete=models.PROTECT,
        verbose_name='Author',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Category',
    )

    def __str__(self):
        return self.title


class ArticleTag(MyBaseModel):
    article = models.ForeignKey(
        Article,
        null=True,
        blank=False,
        on_delete=models.PROTECT,
        verbose_name='Article',
    )
    tag = models.ForeignKey(
        Tag,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Tag',
    )

    def __str__(self):
        return f'{self.tag}'

    class Meta:
        verbose_name = 'Article Tag'
        verbose_name_plural = 'Article Tags'
        ordering = ('id',)


class KeyWordResultItem(MyBaseModel):
    article = models.ForeignKey(
        Article,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Article',
    )

    keyword_result = models.ForeignKey(
        KeyWordResult,
        null=True,
        blank=False,
        on_delete=models.PROTECT,
        verbose_name='Key Word',
    )

    class Meta:
        verbose_name = 'Key Word Result Item'
        verbose_name_plural = 'Key Word Result Items'
        ordering = ('id',)

    def __str__(self):
        return f'{self.keyword_result}'
