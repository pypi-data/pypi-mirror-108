from django.contrib import admin

from djupiter.models import SuperAdmin, Commoner, User


@admin.register(SuperAdmin)
class SuperAdminAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return User.objects.filter(is_superuser=True)


@admin.register(Commoner)
class CommonerAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return User.objects.filter(is_superuser=False)
