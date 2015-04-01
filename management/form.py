#coding=utf-8

from transaction.models import *
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.forms import ModelForm
from django import forms

from management.models import Staff


class StaffRegisterForm(ModelForm):
    username = forms.CharField(label=_(u"用户名"), min_length=6, max_length=30, required=True, widget=forms.TextInput(attrs={'size': 30, }), help_text=u'长度小于30，只限字母、数字及符号@.+-_',
                               validators=[validators.RegexValidator(r'^[\w.@+-]+$', _('请输入合法的用户名'), 'invalid'), ])
    password1 = forms.CharField(label=_(u"密码"), min_length=6, max_length=30, required=True, widget=forms.PasswordInput(attrs={'size': 30, }), help_text=u'密码6-20位，支持字母、数字及符号@.+-_',
                                validators=[validators.RegexValidator(r'^[\w.@+-]+$', _('请输入合法的密码'), 'invalid'), ])
    password2 = forms.CharField(label=_(u"确认密码"), max_length=20, required=True, widget=forms.PasswordInput(attrs={'size': 30, }), help_text=u'重复一遍密码')

    class Meta:
        model = Staff
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StaffRegisterForm, self).__init__(*args, **kwargs)
        # self.fields['hint'].widget.attrs.update({'style': 'display:none;'})

    def clean(self):
        cleaned_data = super(StaffRegisterForm, self).clean()

    # clean()和clean_<field>&()的最后必须返回验证完毕或修改后的值
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        # if len(password1) < 6:
        #     raise forms.ValidationError(_(u'密码长度不够，至少6位'), code='password_not_enough_long', )
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_(u'两次密码输入不一致，请重新输入'), code='password_mismatch')
        return password2
