from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from . import models, forms
from .adminsite import OrderedAdminSite


admin_site = OrderedAdminSite(
    site_header='PROuni. Educational project',
    site_title='PROuni',
    index_title='Адміністрування',
    admin_order=(
        ('web', ('Profile', 'Business')),
        ('auth', ('User', 'Group')),
    ),
    unregister=Group
)


@admin.register(models.Profile, site=admin_site)
class ProfileAdmin(UserAdmin):
    #add_form = forms.CustomUserCreationForm
    #form = forms.CustomUserChangeForm
    model = models.Profile
    list_display = ('email', 'first_name', 'last_name', 'role', 'city')
    list_filter = ('role', 'city')
    search_fields = ('first_name', 'last_name', 'city')
    ordering = ('email',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Права доступа', {'fields': ('role', 'is_active')}),
        ('Персональні дані', {'fields': ('first_name', 'last_name', 'city', 'company', 'scope', 'course')}),
        ('Важливи дати', {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role')}
        ),
    )


@admin.register(models.Opportunity, site=admin_site)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_descr')
#    list_filter = ('city',)
#    search_fields = ('first_name', 'last_name', 'city')
