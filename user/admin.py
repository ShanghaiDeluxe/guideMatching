from django.contrib import admin
from user.models import Language, MyStation, MyUser

admin.site.register(MyUser)
admin.site.register(Language)
admin.site.register(MyStation)
