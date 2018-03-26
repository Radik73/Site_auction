from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Lot, Rate, User
from .models import UserProfile


class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


# Определяем новый класс настроек для модели User
class UserAdmin(UserAdmin):
    inlines = (UserInline,)


# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Lot)
admin.site.register(Rate)
# Register your models here.
