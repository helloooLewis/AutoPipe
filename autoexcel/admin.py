from django.contrib import admin

# Register your models here.
from .models import automodel


class Autoexcel(admin.ModelAdmin):
    list_display = ('pk', 'auto_type', 'func', 'desc',
                    'auther','remarks')
    list_filter = ('auto_type', 'func', 'desc',
                    'auther')
    search_fields = ('auto_type', 'func','remarks')
    ordering = ['pk']
admin.site.register(automodel, Autoexcel)



