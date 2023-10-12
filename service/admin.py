from django.contrib import admin
from .models import UserInfo, UserRequests, ClearPrice, Cart, ClearHistory

admin.site.register(UserInfo)
admin.site.register(UserRequests)
admin.site.register(ClearPrice)
admin.site.register(Cart)
admin.site.register(ClearHistory)
# Register your models here.
