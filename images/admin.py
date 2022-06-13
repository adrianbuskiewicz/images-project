from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Tier, ImageFile, ExpiringLink
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# Register your models here.


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username',)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'tier', 'is_superuser', 'is_staff')
    list_filter = ('username', 'tier', 'is_superuser', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'tier')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'tier', 'is_staff')}
         ),
    )
    ordering = ('is_superuser', 'is_staff', 'username')


class ImageAdmin(admin.ModelAdmin):
    exclude = ['id']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tier)
admin.site.register(ImageFile)
admin.site.register(ExpiringLink)
