from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import Address, Profile, User

User = get_user_model()

# unregister group model
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['email', 'first_name', 'last_name', 'admin']
    list_filter = ['admin']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
         'fields': ('first_name', 'last_name', 'gender')}),
        ('Permissions', {'fields': ('staff', 'admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2', 'first_name', 'last_name', 'gender',  'staff', 'admin')}
         ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()

    class Meta:
        model = User
        fields = ['email']


admin.site.register(Profile)
admin.site.register(Address)
