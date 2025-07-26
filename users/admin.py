from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        'phone_number',
        'email',
        'first_name',
        'last_name',
        'invite_code',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser')

    readonly_fields = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Личная информация', {'fields': ('email', 'first_name', 'last_name', 'invite_code')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone_number',
                'email',
                'first_name',
                'last_name',
                'invite_code',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

    search_fields = ('phone_number', 'email', 'first_name', 'last_name', 'invite_code')
    ordering = ('phone_number',)
