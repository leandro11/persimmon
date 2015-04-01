#coding=utf-8

from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib import admin
from member.models import *
from transaction.models import *
from django.forms import ModelForm
from django import forms


@deconstructible
class UserDuplicateValidator(object):
    message = _(u'该用户名已被使用，请重新选择一个用户名')
    code = u'usernameduplicate'

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        count = User.objects.filter(username=value).count()
        if count > 0:
            raise ValidationError(self.message, code=self.code)


#========================================================= BANK ==========================================================

class BankContactorInline(admin.StackedInline):
    model = BankContactor
    extra = 1
    can_delete = False
    max_num = 1
    exclude = ['user', 'groupname']
    verbose_name_plural = u'银行会员主联络人'


class BankContactorReadonlyInline(admin.StackedInline):
    model = BankContactor
    extra = 1
    can_delete = False
    max_num = 1
    exclude = ['user', 'groupname', 'pwd_question', 'pwd_answer', 'identity_card']
    readonly_fields = ['username', 'name', 'mobile_number', 'telephone', 'email', 'position']
    verbose_name_plural = u'银行会员主联络人'


class BankOperatorForm(forms.ModelForm):
    password1 = forms.CharField(label=_(u"密码"), min_length=6, max_length=30, required=True, widget=forms.PasswordInput(attrs={'size': 30, }),
                                help_text=u'密码6-20位，支持字母、数字及符号@.+-_',
                                validators=[validators.RegexValidator(r'^[\w.@+-]+$', _('请输入合法的密码'), 'invalid'), ])
    password2 = forms.CharField(label=_(u"确认密码"), max_length=20, required=True, widget=forms.PasswordInput(attrs={'size': 30, }), help_text=u'重复一遍密码')

    class Meta:
        model = BankOperator
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        # if len(password1) < 6:
        #     raise forms.ValidationError(_(u'密码长度不够，至少6位'), code='password_not_enough_long', )
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_(u'两次密码输入不一致，请重新输入'), code='password_mismatch')
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        count = User.objects.filter(username=username).count()
        if count > 0:
            raise forms.ValidationError(_(u'用户名重复，请重新选择一个用户名'), code='username_duplicate')
        return username

        # def __init__(self, *args, **kwargs):
        #     super(BankOperatorForm, self).__init__(*args, **kwargs)


class BankOperatorRegisterInline(admin.StackedInline):
    model = BankOperator
    extra = 1
    can_delete = False
    max_num = 3
    exclude = ['user', 'groupname']
    verbose_name_plural = u'银行会员执行人（至多三人）'
    form = BankOperatorForm


class BankOperatorConfirmInline(admin.StackedInline):
    model = BankOperator
    extra = 0
    can_delete = True
    max_num = 3
    exclude = ['user', 'groupname']
    verbose_name_plural = u'银行会员执行人（至多三人）'


class BankRegisterForm(ModelForm):
    strategic_agreements_file = forms.FileField(label=_(u"战略合作协议"), required=True)
    execution_agreements_file = forms.FileField(label=_(u"执行合作协议"), required=True)

    hint = forms.CharField(label=_(u"填写主联络人信息"), max_length=30, required=False, widget=forms.TextInput(attrs={'size': 20, }))
    username = forms.CharField(label=_(u"用户名"), min_length=6, max_length=30, required=True, widget=forms.TextInput(attrs={'size': 30, }), help_text=u'长度小于30，只限字母、数字及符号@.+-_',
                               validators=[validators.RegexValidator(r'^[\w.@+-]+$', _('请输入合法的用户名'), 'invalid'), ])
    password1 = forms.CharField(label=_(u"密码"), min_length=6, max_length=30, required=True, widget=forms.PasswordInput(attrs={'size': 30, }), help_text=u'密码6-20位，支持字母、数字及符号@.+-_',
                                validators=[validators.RegexValidator(r'^[\w.@+-]+$', _('请输入合法的密码'), 'invalid'), ])
    password2 = forms.CharField(label=_(u"确认密码"), max_length=20, required=True, widget=forms.PasswordInput(attrs={'size': 30, }), help_text=u'重复一遍密码')
    contactor_name = forms.CharField(label=_(u"姓名"), min_length=2, max_length=20, required=True, widget=forms.TextInput(attrs={'size': 20, }), help_text=u'主联络人用户名')
    contactor_identity = forms.CharField(label=_(u"身份证"), min_length=15, max_length=20, required=True, widget=forms.TextInput(attrs={'size': 30, }), help_text=u'主联络人身份证号')
    contactor_mobile = forms.CharField(label=_(u"手机"), min_length=11, max_length=11, required=True, widget=forms.TextInput(attrs={'size': 15, }), help_text=u'主联络人手机号')
    contactor_mobile_verify = forms.CharField(label=_(u"手机验证码"), min_length=8, max_length=8, required=True, widget=forms.TextInput(attrs={'size': 8, }), help_text=mark_safe(u'<button onclick="send_sms_verify(this);return false">点击获取</button>'))
    contactor_email = forms.EmailField(label=_(u"电子邮件"), min_length=4, max_length=50, required=True, widget=forms.TextInput(attrs={'size': 30, }), help_text=u'电子邮箱')
    contactor_question = forms.CharField(label=_(u"密保问题"), min_length=3, max_length=100, required=True, widget=forms.TextInput(attrs={'size': 50, }), help_text=u'密码保护问题')
    contactor_answer = forms.CharField(label=_(u"密保答案"), min_length=3, max_length=50, required=True, widget=forms.TextInput(attrs={'size': 30, }), help_text=u'密码保护问题答案')

    class Meta:
        model = Bank
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BankRegisterForm, self).__init__(*args, **kwargs)
        self.fields['hint'].widget.attrs.update({'style': 'display:none;'})
        # 载入空表
        if 'initial' in kwargs:
            invite_code_str = kwargs['initial']['code']
            invite_code = RegisterInvitationCode.objects.get(code=invite_code_str)
            # todo 验证邀请码
            self.fields['name'].initial = invite_code.member_name
        # 有数据POST上来
        if 'instance' in kwargs:
            pass

    def clean(self):
        cleaned_data = super(BankRegisterForm, self).clean()

    # clean()和clean_<field>&()的最后必须返回验证完毕或修改后的值
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        # if len(password1) < 6:
        #     raise forms.ValidationError(_(u'密码长度不够，至少6位'), code='password_not_enough_long', )
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_(u'两次密码输入不一致，请重新输入'), code='password_mismatch')
        return password2


#========================================================= ENTERPRISE ==========================================================

class EnterpriseContactorInline(admin.StackedInline):
    model = EnterpriseContactor
    extra = 1
    can_delete = False
    max_num = 1
    exclude = ['user']
    verbose_name_plural = u'企业会员主联络人'
    readonly_fields = ['username', ]

    class Meta:
        model = EnterpriseOperator
        password1 = forms.CharField(label=_(u"密码"), min_length=6, max_length=30, required=True, widget=forms.PasswordInput(attrs={'size': 30, }),
                                    help_text=u'密码6-20位，支持字母、数字及符号@.+-_',
                                    validators=[validators.RegexValidator(r'^[\w.@+-]+$', _('请输入合法的密码'), 'invalid'), ])
        password2 = forms.CharField(label=_(u"确认密码"), max_length=20, required=True, widget=forms.PasswordInput(attrs={'size': 30, }), help_text=u'重复一遍密码')


class EnterpriseOperatorForm(forms.ModelForm):
    password1 = forms.CharField(label=_(u"密码"), min_length=6, max_length=30, required=True, widget=forms.PasswordInput(attrs={'size': 30, }),
                                help_text=u'密码6-20位，支持字母、数字及符号@.+-_',
                                validators=[validators.RegexValidator(r'^[\w.@+-]+$', _('请输入合法的密码'), 'invalid'), ])
    password2 = forms.CharField(label=_(u"确认密码"), max_length=20, required=True, widget=forms.PasswordInput(attrs={'size': 30, }), help_text=u'重复一遍密码')

    class Meta:
        model = EnterpriseOperator
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_(u'两次密码输入不一致，请重新输入'), code='password_mismatch')
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        count = User.objects.filter(username=username).count()
        if count > 0:
            raise forms.ValidationError(_(u'用户名重复，请重新选择一个用户名'), code='username_duplicate')
        return username


class EnterpriseOperatorRegisterInline(admin.StackedInline):
    model = EnterpriseOperator
    verbose_name = u'企业会员执行人（仅限一名）'
    verbose_name_plural = u'企业会员执行人（仅限一名）'
    extra = 1
    can_delete = False
    max_num = 3
    exclude = ['user', 'groupname']
    verbose_name_plural = u'企业会员执行人'
    form = EnterpriseOperatorForm


class EnterpriseOperatorListInline(admin.TabularInline):
    model = EnterpriseOperator
    readonly_fields = []
    extra = 0
    can_delete = True
    max_num = 3
    exclude = ['user', 'groupname', 'telephone', 'position', 'pwd_question', 'pwd_answer']
    verbose_name_plural = u'银行会员执行人'


class EnterpriseOperatorAddInline(admin.StackedInline):
    model = EnterpriseOperator
    extra = 0
    can_delete = True
    max_num = 1
    exclude = ['user', 'groupname']
    verbose_name_plural = u'添加一个执行人'
    form = EnterpriseOperatorForm

    def get_queryset(self, request):
        """Alter the queryset to return no existing entries"""
        # get the existing query set, then empty it.
        qs = super(EnterpriseOperatorAddInline, self).queryset(request)
        return qs.none()


class EnterpriseOperatorConfirmInline(admin.StackedInline):
    model = EnterpriseOperator
    extra = 0
    can_delete = True
    max_num = 3
    exclude = ['user', 'groupname']
    verbose_name_plural = u'企业会员执行人'


class EnterpriseContactorReadonlyInline(admin.StackedInline):
    model = EnterpriseContactor
    extra = 1
    can_delete = False
    max_num = 1
    exclude = ['user', 'groupname', 'pwd_question', 'pwd_answer', 'identity_card']
    readonly_fields = ['username', 'name', 'mobile_number', 'telephone', 'email', 'position']
    verbose_name_plural = u'银行会员主联络人'


# 会员注册时的表单
class EnterpriseRegisterForm(ModelForm):
    licence_file = forms.FileField(label=_(u"经营执照"), required=True)
    organization_code_file = forms.FileField(label=_(u"组织代码"), required=True)
    tax_registration_file = forms.FileField(label=_(u"税务登记证"), required=True)

    hint = forms.CharField(label=_(u"填写主联络人信息"), max_length=30, required=False, widget=forms.TextInput(attrs={'size': 20, }))
    username = forms.CharField(label=_(u"用户名"), min_length=6, max_length=30, required=True, widget=forms.TextInput(attrs={'size': 30, }), help_text=u'长度小于30，只限字母、数字及符号@.+-_',
                               validators=[validators.RegexValidator(r'^[\w.@+-]+$', _('请输入合法的用户名'), 'invalid'), UserDuplicateValidator()])
    password1 = forms.CharField(label=_(u"密码"), min_length=6, max_length=30, required=True, widget=forms.PasswordInput(attrs={'size': 30, }), help_text=u'密码6-20位，支持字母、数字及符号@.+-_',
                                validators=[validators.RegexValidator(r'^[\w.@+-]+$', _('请输入合法的密码'), 'invalid'), ])
    password2 = forms.CharField(label=_(u"确认密码"), max_length=20, required=True, widget=forms.PasswordInput(attrs={'size': 30, }), help_text=u'重复一遍密码')
    contactor_name = forms.CharField(label=_(u"姓名"), min_length=2, max_length=20, required=True, widget=forms.TextInput(attrs={'size': 20, }), help_text=u'主联络人用户名')
    contactor_identity = forms.CharField(label=_(u"身份证"), min_length=15, max_length=20, required=True, widget=forms.TextInput(attrs={'size': 30, }), help_text=u'主联络人身份证号')
    contactor_mobile = forms.CharField(label=_(u"手机"), min_length=11, max_length=11, required=True, widget=forms.TextInput(attrs={'size': 15, }), help_text=u'主联络人手机号')
    contactor_mobile_verify = forms.CharField(label=_(u"手机验证码"), min_length=8, max_length=8, required=True, widget=forms.TextInput(attrs={'size': 8, }), help_text=mark_safe(u'<button onclick="send_sms_verify(this);return false">点击获取</button>'))
    contactor_email = forms.EmailField(label=_(u"电子邮件"), min_length=4, max_length=50, required=True, widget=forms.TextInput(attrs={'size': 30, }), help_text=u'电子邮箱')
    contactor_question = forms.CharField(label=_(u"密保问题"), min_length=3, max_length=100, required=True, widget=forms.TextInput(attrs={'size': 50, }), help_text=u'密码保护问题')
    contactor_answer = forms.CharField(label=_(u"密保答案"), min_length=3, max_length=50, required=True, widget=forms.TextInput(attrs={'size': 30, }), help_text=u'密码保护问题答案')

    class Meta:
        model = Enterprise
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EnterpriseRegisterForm, self).__init__(*args, **kwargs)
        self.fields['hint'].widget.attrs.update({'style': 'display:none;'})
        # 载入空表
        if 'initial' in kwargs:
            invite_code_str = kwargs['initial']['code']
            # contctor_form = EnterpriseContactorForm()
            # self.fields['username'] = contctor_form.fields['username']
            # self.fields['password'] = contctor_form.fields['password']
            # self.fields['password2'] = contctor_form.fields['password']
            # self.fields.insert(2, contctor_form.fields['password'])
            # self.fields['name'].value = invite_code_str
            # self.fields['hint'].widget.input_type='hidden'
            invite_code = RegisterInvitationCode.objects.get(code=invite_code_str)
            # todo 验证邀请码
            self.fields['name'].initial = invite_code.member_name
        # 有数据POST上来
        if 'instance' in kwargs:
            pass

    def clean(self):
        cleaned_data = super(EnterpriseRegisterForm, self).clean()

    # clean()和clean_<field>&()的最后必须返回验证完毕或修改后的值
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        # if len(password1) < 6:
        #     raise forms.ValidationError(_(u'密码长度不够，至少6位'), code='password_not_enough_long', )
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_(u'两次密码输入不一致，请重新输入'), code='password_mismatch')
        return password2


class BankOperatorListInline(admin.TabularInline):
    model = BankOperator
    readonly_fields = []
    extra = 0
    can_delete = True
    max_num = 0
    exclude = ['user', 'groupname', 'telephone', 'position', 'pwd_question', 'pwd_answer']
    verbose_name_plural = u'银行会员执行人'
    readonly_fields = ['username']

    # todo 添加单个执行人连接


class BankOperatorAddInline(admin.StackedInline):
    model = BankOperator
    extra = 1
    can_delete = True
    max_num = 1
    exclude = ['user', 'groupname', '']
    verbose_name_plural = u'添加一个执行人'
    form = BankOperatorForm

    def get_queryset(self, request):
        """Alter the queryset to return no existing entries"""
        # get the existing query set, then empty it.
        qs = super(BankOperatorAddInline, self).queryset(request)
        return qs.none()


class BankContactorListInline(admin.StackedInline):
    model = BankContactor
    extra = 1
    can_delete = False
    max_num = 1
    exclude = ['user', 'groupname']
    # readonly_fields = '__all__'
    verbose_name_plural = u'银行会员主联络人'


class RegisterInviteCodeChangeForm(ModelForm):
    referee_member = forms.CharField(label=_(u"推荐方"), min_length=2, max_length=20, required=True, widget=forms.TextInput(attrs={'readonly': True, 'style': 'border: 0'}), )
    url = forms.CharField(label=u'注册链接', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly', 'style': 'border:0;width:80%'}))

    class Meta:
        model = RegisterInvitationCode
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RegisterInviteCodeChangeForm, self).__init__(*args, **kwargs)
        # 有数据POST上来
        if 'instance' in kwargs:
            self.fields['url'].initial = kwargs['instance'].url
            if kwargs['instance'].referee_member_type == BANK_MEMBER:
                bank = Bank.objects.get(id=kwargs['instance'].referee_member_id)
                self.fields['referee_member'].initial = u'[银行会员]' + bank.name
            elif kwargs['instance'].referee_member_type == ENTERPRISE_MEMBER:
                enterprise = Enterprise.objects.get(id=kwargs['instance'].referee_member_id)
                self.fields['referee_member'].initial = u'[企业会员]' + enterprise.name


class RegisterInviteCodeShowForm(ModelForm):
    url = forms.CharField(label=u'注册链接', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly', 'style': 'border:0;width:80%'}))

    class Meta:
        model = RegisterInvitationCode
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RegisterInviteCodeShowForm, self).__init__(*args, **kwargs)
        # 有数据POST上来
        if 'instance' in kwargs:
            self.fields['url'].initial = kwargs['instance'].url


class BankAttachmentInline(admin.StackedInline):
    model = BankAttachment
    extra = 0
    can_delete = False
    max_num = 0
    exclude = ['name', 'bank', 'extension', 'size', 'width', 'height', 'thumbnail', 'creator', 'need_login']
    readonly_fields = ['type', 'file']
    verbose_name_plural = u'合作协议'














