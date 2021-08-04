from django.contrib import admin

from accounts.models import User
from accounts.models import Account


admin.site.register(User)
admin.site.register(Account)