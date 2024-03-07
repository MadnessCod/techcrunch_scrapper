from django.contrib import admin
from django.contrib.admin import register

from .models import Category, Author, Tag, KeyWord, KeyWordResult, KeyWordResultItem, Article, ArticleTag


# Register your models here.


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_date', 'is_active', 'is_download')
    list_display_links = ('id', 'title')
    list_filter = ('title', 'created_date', 'updated_date')
    list_editable = ('is_download', 'is_active')
    search_fields = ('title', 'created_date')


@register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_date', 'is_active', 'is_download')
    list_display_links = ('id', 'title')
    list_filter = ('title', 'created_date', 'updated_date')
    list_editable = ('is_download', 'is_active')
    search_fields = ('title', 'created_date')


@register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_date', 'is_active', 'is_download')
    list_display_links = ('id', 'title')
    list_filter = ('title', 'created_date', 'updated_date')
    list_editable = ('is_download', 'is_active')
    search_fields = ('title', 'created_date')


@register(KeyWord)
class KeyWordAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_date', 'is_download', 'is_active',)
    list_display_links = ('id', 'title')
    list_filter = ('title', 'created_date', 'updated_date')
    list_editable = ('is_download', 'is_active')
    search_fields = ('title', 'created_date')


@register(KeyWordResult)
class KeyWordResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'keyword', 'created_date',)
    list_display_links = ('id', 'keyword',)
    list_filter = ('created_date', 'updated_date',)
    search_fields = ('updated_date', 'created_date',)


@register(KeyWordResultItem)
class KeyWordResultItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'keyword_result', 'created_date',)
    list_display_links = ('id', 'keyword_result')
    list_filter = ('keyword_result', 'created_date', 'updated_date')
    search_fields = ('keyword_result', 'created_date')


@register(ArticleTag)
class ArticleTag(admin.ModelAdmin):
    list_display = ('id', 'tag', 'article', 'created_date',)
    list_display_links = ('id', 'tag')
    list_filter = ('created_date', 'updated_date',)
    search_fields = ('created_date',)


@register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'category',
        'posted',
        'created_date',
        'is_download',
        'is_active',
    )
    list_display_links = ('id', 'title', 'author', 'category')
    list_filter = ('category', 'created_date', 'updated_date')
    list_editable = ('is_download', 'is_active')
    search_fields = ('title', 'created_date')
