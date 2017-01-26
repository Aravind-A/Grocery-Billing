from django.conf.urls import url
from .views import login_view,logout_view,dashboard

urlpatterns = [ 
    url(r'^login$',login_view,name='login'),
    url(r'^logout$',logout_view,name='logout'),
    url(r'^dashboard$',dashboard,name='dashboard'),
    ]