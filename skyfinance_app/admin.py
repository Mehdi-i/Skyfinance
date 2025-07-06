from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Balance, Transactions


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth',)}),
        (None, {'fields': ('profile_picture',),}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Balance)
admin.site.register(Transactions)