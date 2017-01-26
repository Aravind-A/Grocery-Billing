from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .models import Employee
# Create your views here.

def login_view(request):
    auth = -1
    if request.method == 'POST':
        uname = request.POST.get('login_username','default')
        upwd = request.POST.get('login_password','default')
        user = authenticate(username=uname, password=upwd)
        if user is not None:
            login(request,user)
            return redirect('/users/dashboard')
        else:
            auth = -2
    return render(request,"index.html", {'auth' : auth })
    
def dashboard(request):
    if request.user.is_authenticated():
        e = get_object_or_404(Employee, user=request.user)
        if e.pos == 'C':
            return render(request,"cashier_dashboard.html",{'emp' : e, 'range' : range(1,3) })
        else:
            return render(request,"search.html",{'emp' : e })
    else:
        return HttpResponse('Please provide your credentials')

def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
        return redirect('/users/login')
    else:
        return HttpResponse('Please provide your credentials')
        
