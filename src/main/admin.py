from django.contrib import admin
from main import models

admin.site.register(models.MyUser)
admin.site.register(models.Reservation)
admin.site.register(models.Rest)
admin.site.register(models.Room)
admin.site.register(models.Office)
