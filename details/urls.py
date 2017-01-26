from django.conf.urls import url
from .views import get_item_details, get_item_price, generate_bill, get_customer, update_stock, get_bills_by_date, bill_detail, add_item, item_list

urlpatterns = [ 
    url(r'^get_item_details$', get_item_details, name='get_item_details'),
    url(r'^get_item_price$', get_item_price, name='get_item_price'),
    url(r'^generate_bill$', generate_bill, name='generate_bill'),
    url(r'^get_customer$', get_customer, name='get_customer'),
    url(r'^update_stock$', update_stock, name='update_stock'),
    url(r'^get_bills_by_date$', get_bills_by_date, name='get_bills_by_date'),
    url(r'^bill_detail$', bill_detail, name='bill_detail'),
    url(r'^add_item$', add_item, name='add_item'),
    url(r'^item_list$', item_list, name='item_list'),
    ]