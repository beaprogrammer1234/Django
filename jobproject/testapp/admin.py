from django.contrib import admin
from testapp.models import Bnglrjobs
# Register your models here.

class JobsAdmin(admin.ModelAdmin):
    list_display = ['date','company','title','eligibility','address','email','phonenumber']

admin.site.register(Bnglrjobs,JobsAdmin)
