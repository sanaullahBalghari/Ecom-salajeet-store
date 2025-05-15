from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(Category)