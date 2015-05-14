DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ttms',
        'USER': 'ttms',
        'PASSWORD': '123456',
        'HOST': 'rdsm2k0ua7g4l8u5rf4qo.mysql.rds.aliyuncs.com',
        'PORT': '3306',
    }
}

# after logined, redirect member to
LOGIN_REDIRECT_URL='/management/login_redirect/'

