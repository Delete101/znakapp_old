from django.contrib import admin
from .models import UserInfo, UserRequests, ClearPrice, Cart

admin.site.register(UserInfo)
admin.site.register(UserRequests)
admin.site.register(ClearPrice)
admin.site.register(Cart)
# Register your models here.
