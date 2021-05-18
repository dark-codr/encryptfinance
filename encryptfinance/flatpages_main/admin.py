#-*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE
from .models import FAQ

class CkeditorFlatpageForm(FlatpageForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    
class CkeditorFlatPageAdmin(FlatPageAdmin):
    form = CkeditorFlatpageForm
    
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CkeditorFlatPageAdmin)
admin.site.register(FAQ)