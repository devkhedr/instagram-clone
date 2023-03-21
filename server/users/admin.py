from django.contrib import admin
from users.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "is_verified", "created"]


admin.site.register(User, UserAdmin)
