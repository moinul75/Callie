from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type', 'image')}),
    )
    list_display = ['username', 'email', 'user_type', 'get_image']
    readonly_fields = ['get_image']

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return 'No image'
    get_image.short_description = 'Profile Picture'

admin.site.register(User, CustomUserAdmin)

