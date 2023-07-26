from django.contrib import admin
from .models import Post

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
