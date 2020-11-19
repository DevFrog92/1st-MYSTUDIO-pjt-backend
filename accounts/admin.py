from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
admin.site.register(User,UserAdmin)
##https://docs.djangoproject.com/en/3.1/topics/auth/customizing/ 참고