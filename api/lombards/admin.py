from django.contrib import admin
from .models import PercentQuery, Filial, GoldMark

class PercentQueryAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )
    list_display = ('id', 'lastName', 'created')

admin.site.register(PercentQuery, PercentQueryAdmin)


class FilialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'workTime', 'daysInterval')

admin.site.register(Filial, FilialAdmin)


class GoldMarkAdmin(admin.ModelAdmin):
    list_display = ('mark', 'name', 'price')

admin.site.register(GoldMark, GoldMarkAdmin)
