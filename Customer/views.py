from http.client import CONTINUE
from itertools import product
from multiprocessing import context
from multiprocessing.dummy import JoinableQueue
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm
from Account.views import login_view
from Agent.models import Customer,Notfifcation
from Agent.views import transactions
from Company.models import Product,Advertisment
from .models import Customer_order, Customer_Transaction
from .form import passwordform
from django.core.mail import send_mail
import requests


from django.shortcuts import render

# Create your views here.


def Customer_dashboard(request):
    try:
        if request.user.groups.all()[0].name == 'Customer':
            customer_orders = Customer_order.objects.filter(
                Customer=request.user.customer).order_by('-date_created')

            trans = {}
            for order in customer_orders:
                trans[order.id] = Customer_Transaction.objects.filter(
                    Customer_order_id=order).order_by('-date_created')

            products = Product.objects.all()
            orders = customer_orders
            total_pending = 0
            total_received = 0
            total_paid = 0
            total_rejected = 0
            total_quantity = []
            # for order in orders:
            #     for product in products:
            #         total_quantity+=getattr(order,product.Product_Name)
            transactions = []
            for key, value in trans.items():
                for val in value:
                    total_paid += val.Total_Amount
                    transactions.append(val)

            for order in orders:

                if order.status == 'Pending':
                    total_pending += 1
                elif order.status == 'Not Recived':
                    total_rejected += 1
                elif order.status == 'Delivered':
                    total_received += 1

            # for transaction in transactions:
            #     total_paid+=transaction.Total_Amount
            adds=Advertisment.objects.all()
            context = {
                'customer_orders': customer_orders,
                'total_payment': total_paid,
                'total_pending': total_pending,
                'total_received': total_received,
                'total_rejected': total_rejected,
                'transactions': transactions,
                'adds':adds,
            }
            return render(request, 'Customer/home.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'permission denied ')
        return redirect('logout')

# User Profile


def show_profile(request):
    try:
        if request.user.groups.all()[0].name == 'Customer':
            customer = Customer.objects.get(id=request.user.customer.id)
            context = {'customer': customer}
            return render(request, 'Customer/profile/show_profile.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'permission denied ')
        return redirect('logout')


def edit_profile(request):
    try:
        if request.user.groups.all()[0].name == 'Customer':
            users = User.objects.get(id=request.user.id)
            context = {
                'users': users,

            }
            if request.method == 'POST':
                users.customer.about = request.POST['about']
                users.customer.phone1 = request.POST['phone1']
                users.customer.phone2 = request.POST['phone2']
            #  admin.Company=request.POST['company']
                users.customer.address = request.POST['address']

                users.customer.facebook = request.POST['facebook']
                users.customer.telegram = request.POST['telegram']
                users.customer.instagrm = request.POST['instagram']
                users.first_name = request.POST['first_name']
                users.last_name = request.POST['last_name']
                users.email = request.POST['email']
                users.customer.save()
                users.save()
                return redirect('show_profile_customer')
            return render(request, 'Customer/profile/edit_profile.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'permission denied ')
        return redirect('logout')


def change_password(request):
    try:
        if request.user.groups.all()[0].name == 'Customer':
            users = User.objects.get(id=request.user.id)
            admin = users.customer

            if request.method == 'POST':
                form = passwordform(request.user, request.POST)
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)  # Important!
                    messages.success(
                        request, 'Your password was successfully updated!')
                    return redirect('show_profile')
                else:
                    messages.error(request, 'Please correct the error below.')
            else:
                form = passwordform(request.user)
            context = {
                'admin': admin,
                'usermodel': users,
                'form': form
            }
            return render(request, 'Customer/profile/chage_password.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'permission denied ')
        return redirect('logout')


def change_profile_pic(request):
    return render(request, 'Customer/profile/edit_profile.html',)


def delete_profile_pic(request):
    return render(request, 'Customer/profile/edit_profile.html',)

# end user profile


def make_order(request):
    try:
        if request.user.groups.all()[0].name == 'Customer':
            products = Product.objects.all()

            context = {
                'all_product': products,

            }

            return render(request, 'Customer/cust_order.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'permission denied ')
        return redirect('logout')


def send_delivery(request):
    try:
        if request.user.groups.all()[0].name == 'Customer':
            users = User.objects.get(id=request.user.id)
            requrd_customer = Customer.objects.get(user=users)
            cust_orders = Customer_order.objects.filter(
                Customer=requrd_customer, status='Delivered').order_by('-date_created')
            transactions = {}
            order_arry = []
            trans_arr = []

            for cust_order in cust_orders:
                transactions[cust_order.id] = Customer_Transaction.objects.get(
                    Customer_order_id=cust_order.id)
                order_arry.append(cust_order)

            for order, transa in transactions.items():
                trans_arr.append(transa)

            data = zip(trans_arr, order_arry)

            # my_transaction = Customer_Transaction.objects.filter(Customer_order_id.Customer=requrd_customer)
            context = {
                # 'all_transaction' :all_transaction,
                'data': data,

            }
            return render(request, 'Customer/send-delivery-status.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'permission denied ')
        return redirect('logout')


def customer_transactions(request):
    try:
        if request.user.groups.all()[0].name == 'Customer':
            users = User.objects.get(id=request.user.id)
            requrd_customer = Customer.objects.get(user=users)
            cust_orders = Customer_order.objects.filter(
                Customer=requrd_customer, status='Pending').order_by('-date_created')
            
            cust_orders_not = Customer_order.objects.filter(
                Customer=requrd_customer, status='Not Recived').order_by('-date_created')
            
                
            transactions = {}
            order_arry = []
            trans_arr = []

            for cust_order in cust_orders:
                try:
                    id = cust_order.id

                    transactions[id] = Customer_Transaction.objects.get(
                        Customer_order_id=cust_order.id)
                    order_arry.append(cust_order)
                    order_arry.append(cust_order)
                
            
                except Exception:
                    pass
            for cust_order in cust_orders_not:
                try:
                    id = cust_order.id

                    transactions[id] = Customer_Transaction.objects.get(
                        Customer_order_id=cust_order.id)
                    order_arry.append(cust_order)
                    order_arry.append(cust_order)
                
            
                except Exception:
                    pass

            for order, transa in transactions.items():

                trans_arr.append(transa)

            context = {

                'transactions': transactions,

            }
            return render(request, 'Customer/pinding.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'permission denied ')
        return redirect('logout')


def customer_recived(request, pk):
    try:
        if request.user.groups.all()[0].name == 'Customer':
            users = User.objects.get(id=request.user.id)
            requrd_customer = Customer.objects.get(user=users)
            recived_order = Customer_order.objects.get(
                Customer=requrd_customer, pk=pk)
            recived_order.status = 'Delivered'
            recived_order.save()
            cust_orders = Customer_order.objects.filter(
                Customer=requrd_customer, status='Pending').order_by('-date_created')

            transactions = {}
            order_arry = []
            trans_arr = []

            for cust_order in cust_orders:
                transactions[cust_order.id] = Customer_Transaction.objects.get(
                    Customer_order_id=cust_order.id)
                order_arry.append(cust_order)
            

            for order, transa in transactions.items():
                trans_arr.append(transa)


            

            context = {
                'transactions': transactions,
            }

            return render(request, 'Customer/pinding.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'permission denied ')
        return redirect('logout')


def recived_transactions_by_customer(request):
    try:
        if request.user.groups.all()[0].name == 'Customer':
            users = User.objects.get(id=request.user.id)
            requrd_customer = Customer.objects.get(user=users)
            cust_orders = Customer_order.objects.filter(
                Customer=requrd_customer, status='Delivered').order_by('-date_created')
            transactions = {}
            order_arry = []
            trans_arr = []

            for cust_order in cust_orders:
                transactions[cust_order.id] = Customer_Transaction.objects.get(
                    Customer_order_id=cust_order.id)
                order_arry.append(cust_order)

            for order, transa in transactions.items():
                trans_arr.append(transa)

            data = zip(trans_arr, order_arry)

            # my_transaction = Customer_Transaction.objects.filter(Customer_order_id.Customer=requrd_customer)
            context = {
                # 'all_transaction' :all_transaction,
                'data': data,

            }
            return render(request, 'Customer/recived_order.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'permission denied ')
        return redirect('logout')


def not_recived_transactions_by_customer(request):
    try:
        if request.user.groups.all()[0].name == 'Customer':
            users = User.objects.get(id=request.user.id)
            requrd_customer = Customer.objects.get(user=users)
            cust_orders = Customer_order.objects.filter(
                Customer=requrd_customer, status='Not Recived').order_by('-date_created')
            transactions = {}
            order_arry = []
            trans_arr = []

            for cust_order in cust_orders:
                transactions[cust_order.id] = Customer_Transaction.objects.get(
                    Customer_order_id=cust_order.id)
                order_arry.append(cust_order)

            for order, transa in transactions.items():
                trans_arr.append(transa)

            data = zip(trans_arr, order_arry)

            # my_transaction = Customer_Transaction.objects.filter(Customer_order_id.Customer=requrd_customer)
            context = {
                # 'all_transaction' :all_transaction,
                'data': data,


            }
            return render(request, 'Customer/not_recived_order.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'permission denied ')
        return redirect('logout')


def customer_not_recived(request, pk):
    try:
        if request.user.groups.all()[0].name == 'Customer':
            users = User.objects.get(id=request.user.id)
            requrd_customer = Customer.objects.get(user=users)
            recived_order = Customer_order.objects.get(
                Customer=requrd_customer, pk=pk)
            recived_order.status = 'Not Recived'
            notification=Notfifcation.objects.create(agent=requrd_customer.Agent,customer=requrd_customer,mssg='Not Recived')
            recived_order.save()
            if notification:
                messages.info(request, 'Not Recived Notification Sent')
            cust_orders = Customer_order.objects.filter(
                Customer=requrd_customer, status='Pending').order_by('-date_created')

            transactions = {}
            order_arry = []
            trans_arr = []

            for cust_order in cust_orders:
                transactions[cust_order.id] = Customer_Transaction.objects.get(
                    Customer_order_id=cust_order.id)
                order_arry.append(cust_order)

            for order, transa in transactions.items():
                trans_arr.append(transa)

            context = {
                'transactions': transactions,

            }

            return redirect('not_recived_transactions_by_customer')
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'permission denied ')
        return redirect('logout')


def order_summer(request):
    try:
        if request.user.groups.all()[0].name == 'Customer':
            ag = Customer_order.objects.create(
                Customer=request.user.customer, status='Pending', driver_status='Not Assigned')
            all_product = Product.objects.all()

            ary1 = []
            ary2 = []
            a = 0
            tl = 0
            arr = {}
            q = 0
            if request.method == 'POST':
                for product in all_product:
                    a = request.POST[product.Product_Name]
                    arr[product.Product_Name] = a
                    tp = product.Price_in_creates * \
                        int(request.POST[product.Product_Name])
                    ary1.append(a)
                    ary2.append(tp)
                    q += int(a)
                    tl = tl+tp

                print(arr)
                for key, value in arr.items():
                    setattr(ag, key, value)
                ag.save()

                obj = {
                    "process": "Cart",
                    "successUrl": "http://192.168.137.76:8002/Customer/success/",
                    "ipnUrl": "http://192.168.137.76:8002/Customer/ipn",
                    "cancelUrl": "http://192.168.137.76:8002/Customer/cancel",
                    "merchantId": "SB1560",
                    "merchantOrderId": ag.id,
                    "expiresAfter": 24,
                    "totalItemsDeliveryFee": 19,
                    "totalItemsDiscount": 1,
                    "totalItemsHandlingFee": 12,
                    "totalItemsTax1": 250,
                    "totalItemsTax2": 0
                }
                cart = {"cartitems": [
                    {"itemId": "sku-01", "itemName": "Beer", "unitPrice": tl, "quantity": 1}, ]}
                mylist = zip(all_product, ary1, ary2)
                context = {
                    'all_product': all_product,

                    'a': a,
                    'ary': ary1,
                    'mylist': mylist,
                    'tl': tl,
                    'obj': obj,
                    'cart': cart,
                    'q': q,

                }
                return render(request, 'Customer/order_summer.html', context)
            return redirect('make_order')
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def success(request):
    try:
        if request.user.groups.all()[0].name == 'Customer':
            ii = request.GET.get('itemId')
            total = request.GET.get('TotalAmount')
            moi = request.GET.get('MerchantOrderId')
            ti = request.GET.get('TransactionId')
            status = request.GET.get('Status')
            TransactionCode = request.GET.get('TransactionCode')
            MerchantCode = request.GET.get('MerchantCode')
            BuyerId = request.GET.get('BuyerId')
            Currency = request.GET.get('Currency')
            if not moi:
                return redirect('')

            url = 'https://testapi.yenepay.com/api/verify/pdt/'
            datax = {
                "requestType": "PDT",
                "pdtToken": "Q1woj27RY1EBsm",
                "transactionId": ti,
                "merchantOrderId": moi
            }
            x = requests.post(url, datax)
            if x.status_code == 200:
                print("It's Paid")
            else:
                print('Invalid payment process')
            Customer_Order = Customer_order.objects.get(id=moi)
            context = {
                'total': total,
                'status': status,
                'TransactionCode': TransactionCode,
                'MerchantCode': MerchantCode,
                'BuyerId': BuyerId,
                'Currency': Currency,
                'moi': moi,
                'Customer_Order': Customer_Order,

            }

            TC = Customer_Transaction.objects.filter(
                TransactionCode=TransactionCode)

            if TC.exists():
                redirect('customer_transactions')
            else:
                Customer_Transaction.objects.create(Customer_order_id=Customer_Order, Paid_status=status,
                                                    Total_Amount=total, TransactionCode=TransactionCode, MarchentId=MerchantCode)
            return render(request, 'Customer/post-payment.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')

# def cancel(request):
#     return render(request, 'Agent/cancel.html')

# def ipn(request):
#     return render(request, 'Agent/ipn.html')
# def manage_customers(request):

#      return render(request,'Agent/manage-customers.html',{})

# def transaction_detail(request,pk):
#     transaction=Agent_Transaction.objects.get(id=pk)
#     products=Product.objects.all()
#     order=Agent_order.objects.get(id=transaction.Agent_order_id.id)
#     price=[]
#     prods=[]
#     quantity=[]
#     sub_total=[]
#     grand_total=0
#     total_quantity=0
#     for product in products:
#         price.append(product.Price_in_creates)
#         prods.append(product.Product_Name)
#         quantity.append(getattr(order,product.Product_Name))
#         sub_total.append(product.Price_in_creates*getattr(order,product.Product_Name))

#         total_quantity+=(getattr(order,product.Product_Name))


#     data=zip(prods,price,quantity,sub_total)
#     context={
#         'transaction':transaction,
#         'data':data,

#         'total_quantity':total_quantity,


#     }
#     return render(request,'Agent/transaction-details.html',context)

def customer_transaction_detail(request, pk):
    try:
        if request.user.groups.all()[0].name == 'Customer':
            transaction = Customer_Transaction.objects.get(id=pk)
            products = Product.objects.all()
            order = Customer_order.objects.get(id=transaction.Customer_order_id.id)
            price = []
            prods = []
            quantity = []
            sub_total = []
            grand_total = 0
            total_quantity = 0
            for product in products:
                price.append(product.Price_in_creates)
                prods.append(product.Product_Name)
                quantity.append(getattr(order, product.Product_Name))
                sub_total.append(product.Price_in_creates *
                                getattr(order, product.Product_Name))

                total_quantity += (getattr(order, product.Product_Name))

            data = zip(prods, price, quantity, sub_total)

            context = {
                'transaction': transaction,
                'data': data,
                'total_quantity': total_quantity,

            }
            return render(request, 'Customer/Customer-transaction-details.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'permission denied ')
        return redirect('logout')
