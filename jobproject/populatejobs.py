import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','jobproject.settings')
django.setup()

from testapp.models import *
from faker import Faker
from random import *
faker=Faker()
def phonenumber():
        d1=randint(7,9)
        num=''+str(d1)
        for i in range(9):
            num=num+str(randint(0,9))
        return int(num)
def populate(n):
        for i in range(n):
            fdate=faker.date()
            fcompany=faker.company()
            ftitle=faker.random_element(elements=('project manager','lead','software engineer'))
            feligibility=faker.random_element(elements=('B.Tech','MCA','MTech'))
            faddress=faker.address()
            femail=faker.email()
            fphonenumber=phonenumber()
            bnglrjobs_records=Bnglrjobs.objects.get_or_create(date=fdate,company=fcompany,title=ftitle,eligibility=feligibility,address=faddress,email=femail,phonenumber=fphonenumber)
populate(30)
