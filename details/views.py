from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Item, Customer, Bill, Purchase
from users.models import Employee
import json
import decimal
import time
from django.db.models import F
# Create your views here.

def get_item_details(request):
    if request.user.is_authenticated() and request.method == 'POST':
        item_id = int(request.POST.get('item_id',-1))
        try:
            i = Item.objects.get(id=item_id)
            responseStr = i.item_name + ";" + str(i.unit_price) + ";" + str(i.qty_avail) + ";" + str(i.discount)
            return HttpResponse(responseStr)
        except Item.DoesNotExist:
            return HttpResponse("No such item")    
                
def get_item_price(request):
    if request.user.is_authenticated() and request.method == 'POST':
        item_qty = int(request.POST.get('item_qty',-1))
        item_id = int(request.POST.get('item_id',-1))
        try:
            i = Item.objects.get(id=item_id)
            if item_qty > i.qty_avail:
                return HttpResponse('N.A.')
            else:
                item_price = item_qty * i.unit_price * (1 - (i.discount / 100))
                return HttpResponse(str(item_price))
        except Item.DoesNotExist:
            return HttpResponse(str(0.00))
            
def generate_bill(request):
    if request.user.is_authenticated() and request.method == 'POST':
        itemJson = request.POST.get('item_dict','default')
        if itemJson == 'default' or itemJson == '-1':
            print itemJson
        else:
            itemDict = json.loads(request.POST.get('item_dict','default'))
            cust_id = int(request.POST.get('cust_id',-1))
            total = float(request.POST.get('hidden_total',-1))
            cashier_id = int(request.POST.get('cashier_id',-1))
            ids = []
            names = []
            qtys = []
            amounts = []
            
            b = Bill()
            #b.bill_date = time.strftime("%d-%m-%Y %H:%M:%S")
            b.bill_total = decimal.Decimal(format(total, '.2f'))
            b.cashier = Employee.objects.get(id=cashier_id)
            
            if cust_id != -1:
                try:
                    c = Customer.objects.get(id=cust_id)
                    b.customer = c
                    customer_name = c.customer_name
                    phone_number = c.phone_number
                    address = c.address
                    old_points = c.points
                    new_points = decimal.Decimal(format(old_points,'.2f')) + decimal.Decimal(format(total/100,'.2f'))
                    c.points = new_points
                    c.save(update_fields = ['points'])
                    
                except Customer.DoesNotExist:
                    customer_name = "NA"
                    phone_number = -1
                    address = "NA"
                    new_points = 0
                    old_points = 0
            else:
                customer_name = "NA"
                phone_number = -1
                address = "NA"
                new_points = 0
                old_points = 0
                
            b.save()
            
            for key in itemDict:
                i = Item.objects.get(id=int(key))
                
                p = Purchase()
                p.bill = b
                p.item = i
                p.qty_purchased = int(itemDict[key])
                p.save()                
                
                ids.append(int(key))
                names.append(i.item_name)
                qtys.append(int(itemDict[key]))
                i.qty_avail = F('qty_avail') - int(itemDict[key])
                i.save(update_fields = ['qty_avail'])
                item_price = int(itemDict[key]) * i.unit_price * (1 - (i.discount / 100))
                amounts.append(item_price)
              
            return render(request,"bill.html",{'details' : zip(ids,names,qtys,amounts), 'customer_name' : customer_name, 'phone_number' : str(phone_number), 'address' : address, 'new_points' : str(new_points), 'old_points' : str(old_points), 'total' : str(total), 'bill_id' : str(b.id), 'date_time' : time.strftime("%d-%m-%Y %H:%M:%S") })
    else:
        return HttpResponse("Please authenticate yourself.")
        
def get_customer(request):
    if request.user.is_authenticated() and request.method == 'POST':
        cid = request.POST.get('customer_id',-1)
        if cid == '':
            return HttpResponse("No customer found")
        customer_id = int(cid)
        try:
            c = Customer.objects.get(id=customer_id)
            customerStr = c.customer_name + ";" + c.phone_number + ";" + c.address + ";" + str(c.points)
            print customerStr
            return HttpResponse(customerStr)
        except Customer.DoesNotExist:
            return HttpResponse("No customer found")
    else:
        return HttpResponse("Please authenticate yourself.")
        
def update_stock(request):
    if request.user.is_authenticated() and request.method == 'POST':
        e = get_object_or_404(Employee, user=request.user)
        itemId = int(request.POST.get('ItemId',-1))
        itemQty = int(request.POST.get('Qty',-1))
        i = Item.objects.get(id=itemId)
        i.qty_avail = itemQty
        i.save(update_fields = ['qty_avail'])
        return render(request,"update.html",{'emp' : e, 'updated' : 1, 'added' : 0})
    elif request.user.is_authenticated():
        e = get_object_or_404(Employee, user=request.user)
        return render(request,"update.html",{'emp' : e, 'updated' : 0, 'added' : 0})
    else:
        return HttpResponse("Please authenticate yourself.")
        
def get_bills_by_date(request):
    if request.user.is_authenticated() and request.method == 'POST':
        dateUnicode = request.POST.get('bill_date','default')
        dateStr = str(dateUnicode)
        date = dateStr[3:5]
        month = dateStr[0:2]
        year = dateStr[6:10]
        print date + " " + month + " " + year
        
        bill_ids = []
        bill_totals = []
        bill_customers = []
        bill_cashiers = []
        bill_items = []
        customer_valid = []
        
        b = Bill.objects.all()
        for obj in b:
            bill_date = str(obj.bill_date)
            if bill_date[8:10] == date and bill_date[5:7] == month and bill_date[0:4] == year:
               bill_ids.append(obj.id)
               bill_totals.append(obj.bill_total)
               if obj.customer == None:
                   bill_customers.append({"ID" : -1})
                   customer_valid.append(0)
               else:
                   customerDict = {}
                   customerDict["ID"] = obj.customer.id
                   customerDict["Name"] = obj.customer.customer_name 
                   bill_customers.append(customerDict)
                   customer_valid.append(1)
               cashierDict = {}
               cashierDict[obj.cashier.id] = obj.cashier.name
               bill_cashiers.append(cashierDict)
               
               itemDict = {}
               billItems = Purchase.objects.filter(bill=obj)
               for item in billItems:
                   itemDict[item.item.item_name] = item.qty_purchased
               bill_items.append(itemDict)
        if len(bill_ids) == 0:
            return HttpResponse("No bills on " + dateStr)
        else:
            return render(request,"daily_sales.html",{ 'first' : zip(bill_ids,bill_totals,bill_customers,bill_cashiers,range(1,len(bill_ids)+1),bill_items,customer_valid), 'date' : dateStr })
    else:
        return HttpResponse("Please authenticate yourself.")
        
def bill_detail(request):
    if request.user.is_authenticated() and request.method == 'POST':
        billId = int(request.POST.get('BillNo',-1))
        try:
            b = Bill.objects.get(id=billId)
            b_date = str(b.bill_date)
            b_total = b.bill_total
            if b.customer == None:
                b_customerId = -1
                b_customerName = "NA"
            else:
                b_customerId = b.customer.id
                b_customerName = b.customer.customer_name
            b_cashierId = b.cashier.id
            b_cashierName = b.cashier.name
            item_ids = []
            item_names = []
            item_qtys = []
            item_amounts = []
            purchase = Purchase.objects.filter(bill = b)
            for p in purchase:
                item_ids.append(p.item.id)
                item_names.append(p.item.item_name)
                item_qtys.append(p.qty_purchased)
                item_amounts.append(p.qty_purchased * p.item.unit_price * (1 - (p.item.discount / 100)))
            return render(request,"bill_detail.html",{'details' : zip(item_ids,item_names,item_qtys,item_amounts), 'id' : billId, 'date' : b_date, 'total' : b_total, 'customerId' : b_customerId, 'customerName' : b_customerName, 'cashierId' : b_cashierId, 'cashierName' : b_cashierName })
        except Bill.DoesNotExist:
            return HttpResponse("There is no Bill with ID " + str(billId))
    else:
        return HttpResponse("Please authenticate yourself.")
        
def add_item(request):
    if request.user.is_authenticated() and request.method == 'POST':
        e = get_object_or_404(Employee, user=request.user)
        item_name = request.POST.get('item_name','default')
        unit_price = request.POST.get('unit_price',-1)
        qty_avail = request.POST.get('qty_avail',-1)
        discount = request.POST.get('discount',-1)
        i = Item()
        i.item_name = item_name
        i.unit_price = unit_price
        i.qty_avail = qty_avail
        i.discount = discount
        i.save()
        return render(request,"update.html",{'emp' : e, 'updated' : 0, 'added' : 1})
    else:
        return HttpResponse("Please authenticate yourself.")

def item_list(request):
    if request.user.is_authenticated():
        items = Item.objects.all()
        ids = []
        names = []
        qtys = []
        prices = []
        discounts = []
        for i in items:
            ids.append(i.id)
            names.append(i.item_name)
            qtys.append(i.qty_avail)
            prices.append(i.unit_price)
            discounts.append(i.discount)
        return render(request,"item_list.html",{ 'details' : zip(ids,names,prices,qtys,discounts)})
    else:
        return HttpResponse("Please authenticate yourself.")
            
        
            
            