from django.contrib import admin
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']

class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image', 'uploaded_at', 'description', 'is_active', 'category']
    list_editable = ['is_active']
    list_filter = ['is_active', 'category']
    search_fields = ['title', 'description']

class HelpIconContentAdmin(admin.ModelAdmin):
    list_display = ['content']
    search_fields = ['content']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(HelpIconContent, HelpIconContentAdmin)