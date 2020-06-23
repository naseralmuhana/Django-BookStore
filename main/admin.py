from django.contrib import admin
from main import models

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'Publication_date', 'active']
    list_filter = ['Publication_date',
                   'categories', 'year', 'authors', 'language']
    # readonly_fields = ('page',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'rating']
    list_filter = ['user', 'book', 'rating']
    # readonly_fields = ('rating', 'message')


admin.site.register(models.Category)
admin.site.register(models.Language)
admin.site.register(models.Author)
admin.site.register(models.Year)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Comment, CommentAdmin)
