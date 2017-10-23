from django.shortcuts import render, redirect
from .models import User
# Create your views here.
def index(request):

    return render(request, "landr/index.html")
def register(request):
    if request.method!='POST':
        return redirect('/')
    response_from_model=User.objects.validate_user_r(request.POST)
    if response_from_model['status']:
        request.session['user_id']=response_from_model['id']
        return redirect('/success')
    return redirect('/')
def login(request):
    if request.method!='POST':
        return redirect('/')
    response_from_model=User.objects.validate_user_l(request.POST)
    if response_from_model['status']:
        request.session['user_id']=response_from_model['id']
        return redirect('/success')
    return redirect('/')
def success(request):
    if 'user_id' in request.session:
        return render(request,'landr/success.html')
    return redirect('/')
