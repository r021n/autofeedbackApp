from django.contrib import admin
from .models import Topics, Questions, Answers
# Register your models here.
admin.site.register(Topics)
admin.site.register(Questions)
admin.site.register(Answers)
