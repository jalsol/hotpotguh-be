from django.contrib import admin
from .models import User, Tree, Vendor

# Register your models here.
admin.site.register(User)
admin.site.register(Tree)
admin.site.register(Vendor)
