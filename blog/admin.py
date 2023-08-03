from django.contrib import admin
from .models import Post, Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['POSTitle', 'POSSlug', 'POSAuthor', 'POSPublish', 'POSStatus']
    list_filter = ['POSStatus', 'POSCreated', 'POSPublish', 'POSAuthor']
    search_fields = ['POSTitle', 'POSBody']
    prepopulated_fields = {'POSSlug': ('POSTitle',)}
    raw_id_fields = ['POSAuthor']
    date_hierarchy = 'POSPublish'
    ordering = ['POSStatus', 'POSPublish']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['COMName', 'COMEmail', 'COMPost', 'COMCreated', 'COMActive']
    list_filter = ['COMActive', 'COMCreated', 'COMUpdated']
    search_fields = ['COMName', 'COMEmail', 'COMBody']
