from django.contrib import admin
from demo.models import *
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Category)
#admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(ItemInOrder)

# Register your models here.
