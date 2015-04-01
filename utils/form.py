#coding=utf-8
# -*- coding: utf-8 -*-\

from utils.models import *
from django import forms


class ReadOnlyForm(forms.ModelForm):
    """Base class for making a form readonly."""

    def __init__(self, *args, **kwargs):
        from django.utils.translation import ugettext as _
        from django.forms.widgets import Select

        super(ReadOnlyForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].label = _(self.fields[f].label)
            if isinstance(self.fields[f].widget, Select):
                self.fields[f].widget.attrs['disabled'] = 'disabled'
            else:
                self.fields[f].widget.attrs['readonly'] = 'readonly'
                self.fields[f].widget.attrs['style'] = 'border:0'


class TemplateAttachmentChangeForm(forms.ModelForm):
    link = forms.CharField(label=u'下载链接', widget=forms.TextInput(attrs={'readonly': 'readonly', 'style': 'border:0;width:80%'}))
    thumbnail_link = forms.CharField(label=u'缩略图链接',required=False, widget=forms.TextInput(attrs={'readonly': 'readonly', 'style': 'border:0;width:80%'}))

    class Meta:
        model = TemplateAttachment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TemplateAttachmentChangeForm, self).__init__(*args, **kwargs)
        self.fields['link'].initial = self.instance.get_url
        self.fields['thumbnail_link'].initial = self.instance.get_thumbnail_url

