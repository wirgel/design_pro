from django.contrib import admin
# from django.contrib.auth.models import User
from .models import  Application, Category

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id', 'author', 'title', 'status')
    list_filter = ('author', 'title', 'status')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass