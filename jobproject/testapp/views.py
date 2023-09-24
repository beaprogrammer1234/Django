from django.shortcuts import render
from testapp.models import Bnglrjobs
# Create your views here.
def index(request):
    return render(request,'testapp/home.html')

def bgnlr_view(request):
    jobs_list=Bnglrjobs.objects.order_by('date')
    my_dict={'jobs_list':jobs_list}
    return render(request,'testapp/bnglrjobs.html',my_dict)