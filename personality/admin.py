from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from personality.models import User
from .models import Role,City,Metro,Location

admin.site.register(Role)
admin.site.register(City)
admin.site.register(Metro)
admin.site.register(Location)



# Now register the new UserAdmin...
admin.site.register(User)
#admin.site.register(Auth)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
