from django.contrib import admin
from .models import Package, PurchasePackage, Activity


# Register your models here.


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'activity']


@admin.register(PurchasePackage)
class PurchasePackage(admin.ModelAdmin):
    list_display = ['id', 'get_user', 'get_name']

    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'Username'

    def get_name(self, obj):
        return obj.name
    get_name.short_description = 'Package'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'get_user']

    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'Username'
    get_user.admin_order_field = 'user'