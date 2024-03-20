from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email', 'userID', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'userID',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('email',)  

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
   
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'userID', 'password1', 'password2'),
        }),
    )

admin.site.register(Account, AccountAdmin)