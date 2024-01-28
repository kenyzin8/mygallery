from django.contrib import admin
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']

class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image', 'thumbnail', 'uploaded_at', 'description', 'is_active', 'category']
    list_editable = ['is_active', 'image', 'category']
    list_filter = ['is_active', 'category']
    search_fields = ['title', 'description']
    exclude = ('thumbnail', 'image_height', 'image_width')

class HelpIconContentAdmin(admin.ModelAdmin):
    list_display = ['content']
    search_fields = ['content']

    def has_add_permission(self, request, obj=None):
        if HelpIconContent.objects.exists():
            return False
        return super().has_add_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False

class GridColumnsAdmin(admin.ModelAdmin):
    list_display = ['number_of_columns']
    search_fields = ['number_of_columns']

    def has_add_permission(self, request, obj=None):
        if GridColumns.objects.exists():
            return False
        return super().has_add_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(HelpIconContent, HelpIconContentAdmin)
admin.site.register(GridColumns, GridColumnsAdmin)

admin.site.site_header = "Zin Photos Admin"
admin.site.site_title = "Zin Photos Admin Portal"
admin.site.index_title = "Welcome to Zin Photos Portal"