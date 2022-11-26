from django.contrib import admin
from .models import User, BaseTree, Tree, Vendor

# Register your models here.
admin.site.register(User)
admin.site.register(BaseTree)
admin.site.register(Tree)
admin.site.register(Vendor)
