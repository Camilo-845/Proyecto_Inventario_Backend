from django.contrib import admin
from .models import User
from .models import Item
from .models import Transaction
# Register your models here.

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Transaction)
