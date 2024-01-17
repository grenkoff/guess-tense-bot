from django.contrib import admin

from . import models

class SentenceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'tense', 'sentence']
    list_editable = ['tense', 'sentence']

admin.site.register(models.Sentences, SentenceAdmin)