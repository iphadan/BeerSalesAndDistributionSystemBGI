
from multiprocessing import context
from operator import attrgetter
from statistics import quantiles
from django import http
from django.forms import EmailField
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .form import *
from .models import *
from Company.models import *
from Customer.models import Customer_order, Customer_Transaction
import requests
from passlib.hash import pbkdf2_sha256
import json
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
# Dashbord part

def Agent_dashboard(request):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            context = {}
            try:
                users = User.objects.get(id=request.user.id)

            except users.DoesNotExist:
                return HttpResponse('404,User: Data Not Found')

            try:
                total_pending_order = 0
                table_data = {}
                Total = 0
                arrimg = []
                arrvalu = []
                arrkey = []

                if request.user.groups.all()[0].name == 'Agent':
                    all_Product = Product.objects.all()
                    user = User.objects.get(id=request.user.id)
                    agent = Agent.objects.get(user=user)
                    spesific_store_agent = Agent_Store.objects.get(agent=agent)

                    product_amount = Product_Amount_in_Store_agent.objects.get(
                        store=spesific_store_agent)

                    refile_product = add_to_store_agent.objects.filter(
                        Store=spesific_store_agent).order_by('-date_created')

                    for product in all_Product:
                        arrimg.append(product.img)
                        table_data[product.Product_Name] = (
                            (getattr(product_amount, product.Product_Name)))
                        Total += getattr(product_amount, product.Product_Name)

                request_agent = Agent.objects.filter(user=users)
                all_customer = Customer.objects.filter(Agent=request_agent[0])
                all_vechil = Vehicle.objects.filter(Agent=request_agent[0])
                all_driver = Driver.objects.filter(Agent=request_agent[0])
                total_vichel = all_vechil.count()
                total_driver = all_driver.count()
                print(total_driver)
                print(total_vichel)
                total_customer = all_customer.count()
                penndig_order_customer = []
                agent_custome = []
                cust_order = {}
                customer_order = []
                customer_transaction = []
                for agent_cust in all_customer:
                    cust_order[agent_cust] = Customer_order.objects.filter(
                        Customer=agent_cust)
                for customer, order in cust_order.items():

                    for ord in order:
                        customer_order.append(ord)
                        try:
                            Customer_Transaction.objects.get(
                                Customer_order_id=ord.id)
                            if ord.status == 'Pending':
                                total_pending_order = total_pending_order + 1
                        except Exception as e:
                            continue
                        customer_transaction.append(
                            Customer_Transaction.objects.get(Customer_order_id=ord.id))

                data = zip(customer_order, customer_transaction)

                # penndig_order_customer.append(Customer_order.objects.filter(Customer=customer,status='Pending'))

                adds = Advertisment.objects.all()
                context = {
                    'all_customer': all_customer,
                    'total_customer': total_customer,
                    'adds': adds,
                    'data': data,
                    'cust_order': cust_order,
                    'total_pending_order': total_pending_order,
                    'penndig_order_customer': penndig_order_customer,
                    'total_vichel': total_vichel,
                    'total_driver': total_driver,
                    'Total': Total,


                }
                return render(request, 'Agent/agent-dashboard.html', context)
            except UnboundLocalError as e:
                return HttpResponse('404,User: Data Not Found')
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def my_draiver(request):

    return render(request, 'Agent/my_draiver.html', {})


def my_vichile(request):

    return render(request, 'Agent/my_vichile.html', {})


def my_product(request):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            context = {}
            try:
                users = User.objects.get(id=request.user.id)

            except users.DoesNotExist:
                return HttpResponse('404,User: Data Not Found')

            try:
                total_pending_order = 0
                table_data = {}
                Total = 0
                arrimg = []
                arrvalu = []
                arrname = []

                arrkey = []

                if request.user.groups.all()[0].name == 'Agent':
                    all_Product = Product.objects.all()
                    user = User.objects.get(id=request.user.id)
                    agent = Agent.objects.get(user=user)
                    spesific_store_agent = Agent_Store.objects.get(agent=agent)

                    product_amount = Product_Amount_in_Store_agent.objects.get(
                        store=spesific_store_agent)

                    refile_product = add_to_store_agent.objects.filter(
                        Store=spesific_store_agent).order_by('-date_created')

                    for product in all_Product:
                        arrimg.append(product.img)
                        arrname.append(product.Product_Name)
                        table_data[product.Product_Name] = (
                            (getattr(product_amount, product.Product_Name)))
                        Total += getattr(product_amount, product.Product_Name)

                        arrvalu.append(
                            getattr(product_amount, product.Product_Name))
                data1 = zip(arrimg, arrname, arrvalu)
                request_agent = Agent.objects.filter(user=users)
                all_customer = Customer.objects.filter(Agent=request_agent[0])
                all_vechil = Vehicle.objects.filter(Agent=request_agent[0])
                all_driver = Driver.objects.filter(Agent=request_agent[0])
                total_vichel = all_vechil.count()
                total_driver = all_driver.count()
                print(total_driver)
                print(total_vichel)
                total_customer = all_customer.count()
                penndig_order_customer = []
                agent_custome = []
                cust_order = {}
                customer_order = []
                customer_transaction = []
                for agent_cust in all_customer:
                    cust_order[agent_cust] = Customer_order.objects.filter(
                        Customer=agent_cust)
                for customer, order in cust_order.items():

                    for ord in order:
                        customer_order.append(ord)
                        try:
                            Customer_Transaction.objects.get(
                                Customer_order_id=ord.id)
                            if ord.status == 'Pending':
                                total_pending_order = total_pending_order + 1
                        except Exception as e:
                            continue
                        customer_transaction.append(
                            Customer_Transaction.objects.get(Customer_order_id=ord.id))

                data = zip(customer_order, customer_transaction)

                # penndig_order_customer.append(Customer_order.objects.filter(Customer=customer,status='Pending'))

                adds = Advertisment.objects.all()
                context = {
                    'all_customer': all_customer,
                    'total_customer': total_customer,
                    'adds': adds,
                    'data': data,
                    'cust_order': cust_order,
                    'total_pending_order': total_pending_order,
                    'penndig_order_customer': penndig_order_customer,
                    'total_vichel': total_vichel,
                    'total_driver': total_driver,
                    'Total': Total,
                    'arrimg': arrimg,
                    'data1': data1,


                }
                return render(request, 'Agent/my_product.html', context)

            except UnboundLocalError as e:
                return HttpResponse('404,User: Data Not Found')
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


# ///////////////////////////////////////////////////////////////  user profile part  ////////////////////////////////////////////////////////////////////////////

def show_profile(request):

    try:
        if request.user.groups.all()[0].name == 'Agent':
            users = User.objects.get(id=request.user.id)

            Agent = users.agent

            context = {
                'admin': Agent,
            }
            return render(request, 'Agent/profile/show_profile.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def edit_profile(request):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            users = User.objects.get(id=request.user.id)
            admin = users.agent
            context = {
                'admin': admin,

            }
            if request.method == 'POST':
                admin.about = request.POST['about']
                admin.phone1 = request.POST['phone']
                admin.address = request.POST['address']
                admin.facebook = request.POST['facebook']
                admin.telegram = request.POST['telegram']
                admin.instagram = request.POST['instagram']
                users.first_name = request.POST['first_name']
                users.last_name = request.POST['last_name']

                Email = request.POST['email']
                # email uniqueness
                # email_user=User.objects.get(email=Email)
                users.email = request.POST['email']
                new = User.objects.filter(email=Email)
                x = new.count()
                if x > 1:
                    messages.error(request, 'Email Already Exist')
                    return render(request, 'Agent/profile/edit_profile.html', context)

                admin.save()
                users.save()
                return redirect('show_profile_agent')
            return render(request, 'Agent/profile/edit_profile.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def change_password(request):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            users = User.objects.get(id=request.user.id)
            admin = users.agent

            if request.method == 'POST':
                form = passwordform(request.user, request.POST)
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)  # Important!
                    messages.success(
                        request, 'Your password was successfully updated!')
                    return redirect('show_profile_agent')
                else:
                    messages.error(request, 'Please correct the error below.')
            else:
                form = passwordform(request.user)
            context = {
                'admin': admin,
                'usermodel': users,
                'form': form
            }
            return render(request, 'Agent/profile/chage_password.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def change_profile_pic(request):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            users = User.objects.get(id=request.user.id)
            admin = users.agent
            context = {
                'admin': admin,
                'usermodel': users
            }
            if request.method == 'POST':
                if len(request.FILES['img']) != 0:
                    admin.profile_pic.delete()
                    admin.profile_pic = request.FILES['img']
                    admin.save()
                    return redirect('edit_profile_agent')
                else:
                    return render(request, 'Agent/profile/change_profile_pic.html', context)

            return render(request, 'Agent/profile/change_profile_pic.html', context)

        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def delete_profile_pic(request):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            users = User.objects.get(id=request.user.id)
            admin = users.agent
            context = {
                'admin': admin,
                'usermodel': users
            }
            if len(admin.profile_pic) != 0:
                admin.profile_pic.delete()
                return redirect('edit_profile_agent')

            return render(request, 'Agent/profile/edit_profile.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')

# /////////////////////////////////////////////////////////////// end user profile part ////////////////////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////// Customer Order ///////////////////////////////////////////////////////////////////////////////////


def customer_order(request):
    try:

        if request.user.groups.all()[0].name == 'Agent':
            cust_order = {}
            customer_order = []
            agent_custome = []
            cust_tran = []
            request_agent = Agent.objects.filter(user=request.user)
            all_customer = Customer.objects.filter(Agent=request_agent[0])
            total_customer = all_customer.count()
            penndig_order_customer = []
            agent_custome = []
            cust_order = {}
            customer_order = []
            customer_transaction = []
            for agent_cust in all_customer:
                cust_order[agent_cust] = Customer_order.objects.filter(
                    Customer=agent_cust)

            for customer, order in cust_order.items():

                for ord in order:
                    customer_order.append(ord)
                    try:
                        Customer_Transaction.objects.get(
                            Customer_order_id=ord.id)
                    except Exception as e:
                        continue
                    customer_transaction.append(
                        Customer_Transaction.objects.get(Customer_order_id=ord.id))

                data = zip(customer_order, customer_transaction)

            context = {

                'cust_order': cust_order,
                'data': data,
                'customer_order': customer_order
            }

            return render(request, 'Agent/view-cust-orders.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')

# //////////////////////////////////////////////////////////////////////////////////// End Customer Order ////////////////////////////////////////////////////////////////////


# //////////////////////////////////////////////////////////////////////////////////// cusomer_order_ditel////////////////////////////////////////////////////////////////////

def cusomer_order_ditel(request, pk):

    try:
        if request.user.groups.all()[0].name == 'Agent':
            request_agent = Agent.objects.get(user=request.user)

            try:
                drivers = Driver.objects.filter(Agent=request_agent)

            except ValueError as e:
                drivers = ''

            try:

                transaction = Customer_Transaction.objects.get(id=pk)
                print(transaction)

            except AttributeError as e:
                return ('customer_order')
            products = Product.objects.all()

            order = Customer_order.objects.get(
                id=transaction.Customer_order_id.id)
            if request.method == 'POST':
                driver_id = request.POST.get('driver')
                driver = Driver.objects.get(id=driver_id)
                driver.Status = 'on_duty'
                order.driver_status = 'Assigned'
                order.driver = driver
                order.save()
                driver.save()
                messages.success(request, 'driver sucessfully assigned')
                return redirect('customer_order')

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
                'drivers': drivers,
            }
            return render(request, 'Agent/customer_order_ditel.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')
# ////////////////////////////////////////////////////////////////////////////// End cusomer_order_ditel /////////////////////////////////////////////////////////////////////////


# ////////////////////////////////////////////////////////////////////////////// make_order /////////////////////////////////////////////////////////////////////////

def make_order(request):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            all_product = Product.objects.all()
            all_store = Company_Store.objects.all()
            context = {
                'all_product': all_product,
                'all_store': all_store,

            }
            return render(request, 'Agent/agent_order.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')

# ////////////////////////////////////////////////////////////////////////////// End make_order /////////////////////////////////////////////////////////////////////////


# ////////////////////////////////////////////////////////////////////////////// order_summer /////////////////////////////////////////////////////////////////////////
def order_summer(request):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            all_product = Product.objects.all()
            all_store = Company_Store.objects.all()
            ary1 = []
            ary2 = []
            q = 0
            a = 0
            tl = 0
            arr = {}
            arr3 = []
            if request.method == 'POST':
                store = request.POST['store']
                storee = Company_Store.objects.get(Store_Name=store)
                ag = Agent_order.objects.create(status='Pending', Store=storee)
                for product in all_product:
                    a = request.POST[product.Product_Name]
                    arr[product.Product_Name] = a
                    tp = product.Price_in_creates * \
                        int(request.POST[product.Product_Name])
                    ary1.append(a)
                    ary2.append(tp)
                    tl = tl+tp
                    q += int(a)
                    vat = 0.15 * tl
                for key, value in arr.items():
                    setattr(ag, key, value)
                ag.save()

                obj = {
                    
                    "process": "Cart",
                    "successUrl": "http://192.168.1.128:8002/Agent/success/",
                    "ipnUrl": "http://192.168.137.76:8002/Agent/ipn",
                    "cancelUrl": "http://192.168.137.76:8002/Agent/cancel",
                    "merchantId": "SB1560",
                    "merchantOrderId": ag.id,
                    "expiresAfter": 24,
                    "totalItemsDeliveryFee": 0,
                    "totalItemsDiscount": 0,
                    "totalItemsHandlingFee": 0,
                    "totalItemsTax1": vat,
                    "totalItemsTax2": 0
                }
                cart = {"cartitems": [
                    {"itemId": "sku-01", "itemName": "Beer", "unitPrice": tl, "quantity": 1}, ]}
                mylist = zip(all_product, ary1, ary2)
                context = {
                    'all_product': all_product,
                    'all_store': all_store,
                    'a': a,
                    'ary': ary1,
                    'mylist': mylist,
                    'tl': tl,
                    'obj': obj,
                    'cart': cart,
                    'q': q


                }
                return render(request, 'Agent/order_summer.html', context)
            return redirect('agent_make_order')
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')

# ///////////////////////////////////////////////////////////////////////////////////////// end order_summer /////////////////////////////////////////////////////////


def success(request):

    if request.user.groups.all()[0].name == 'Agent':
        ii = request.GET.get('itemId')
        total = request.GET.get('TotalAmount')
        moi = request.GET.get('MerchantOrderId')
        ti = request.GET.get('TransactionId')
        status = request.GET.get('Status')
        TransactionCode = request.GET.get('TransactionCode')
        MerchantCode = request.GET.get('MerchantCode')
        BuyerId = request.GET.get('BuyerId')
        Currency = request.GET.get('Currency')

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
        Agent_Orders = Agent_order.objects.get(id=moi)
        context = {
            'total': total,
            'status': status,
            'TransactionCode': TransactionCode,
            'MerchantCode': MerchantCode,
            'BuyerId': BuyerId,
            'Currency': Currency,
            'moi': moi,
            'Agent_Orders': Agent_Orders,

        }

        TC = Agent_Transaction.objects.filter(
            TransactionCode=TransactionCode)

        if TC.exists():
            redirect('transactions')
        else:
            Agent_Transaction.objects.create(Agent_order_id=Agent_Orders, Total_Amount=total,
                                             Paid_status=status, TransactionCode=TransactionCode, MarchentId=MerchantCode)
        return render(request, 'Agent/new_post-payment.html', context)
    messages.error(request, 'permission denied ')
    return redirect('logout')


def cancel(request):
    return render(request, 'Agent/cancel.html')


def ipn(request):
    return render(request, 'Agent/ipn.html')


def manage_customers(request):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            users = User.objects.get(id=request.user.id)
            print(users)
            request_agent = Agent.objects.get(user=users)
            all_customer = Customer.objects.filter(Agent=request_agent)
            total_customer = all_customer.count()

            context = {
                'all_customer': all_customer,
                'total_customer': total_customer,
            }
            return render(request, 'Agent/manage-customers.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def add_customers(request):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            ###############################
            if request.method == 'POST':

                errorr = request.POST.get('error')

                # required

                address = request.POST.get('address')

                TIN_NO = request.POST.get('TIN_NO')
                marchent_id = request.POST.get('marchent_id')
                company_name = request.POST.get('company_name')
                license = request.FILES.get('license')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                house_no = request.POST.get('house_no')
                email = request.POST.get('email')
                username = request.POST.get('username')
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                phone1 = request.POST.get('phone1')
                phone2 = request.POST.get('phone2')
                # check if it the followings are empty
                phone1 = phone1
                phone2 = phone2

                profile = request.FILES.get('profile')
                print(errorr)
                if errorr == '':
                    if password1 == password2:
                        new = User.objects.filter(username=username)
                        if new.count():
                            messages.error(request, "User Already Exist")

                        else:
                            new = User.objects.filter(email=email)
                            if new.count():
                                messages.error(request, "email Already Exist")
                            else:

                                user = User.objects.create_user(
                                    username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
                                user.save()
                                print('**************')
                                print(user)
                                print('**************')
                                my_group = Group.objects.get(name='Customer')
                                my_group.user_set.add(user)
                                if user:
                                    customer = Customer.objects.create(user=user, Agent=request.user.agent,
                                                                       Compan_name=company_name, phone1=phone1, phone2=phone2, Address=address,
                                                                       House_No=house_no, profile_pic=profile, TIN_NO=TIN_NO, License=license, Marchent_id=marchent_id)
                                    if customer:
                                        messages.success(
                                            request, 'Agent registered successfully!')
                                        return redirect('manage_customers')

                    else:
                        messages.error(request, 'password didn\'t match.')
                else:
                    messages.error(request, 'Please, fill the form correctly.')

                context = {

                    'address': address,
                    'house_no': house_no,
                    'TIN_NO': TIN_NO,
                    'marchent_id': marchent_id,

                    'license': license,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'username': username,
                    'password1': password1,
                    'phone1': phone1,
                    'phone2': phone2,
                }
                return render(request, 'Agent/add-customer.html', context)

            ###########################################

            return render(request, 'Agent/add-customer.html')
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def customers_ditel(request, pk):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            customer = Customer.objects.get(id=pk)
            orders = Customer_order.objects.filter(Customer=customer)
            all_transaction = []
            for order in orders:
                all_transaction.append(
                    Customer_Transaction.objects.get(Customer_order_id=order.id))
            context = {
                'customer': customer,
                'all_transaction':all_transaction,
            }
            print(all_transaction)
            return render(request, 'Agent/customer-ditel.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def customers_delete(request, pk):
    pass
#     customer=Customer.objects.get(id=pk)
#     customer.delete()
#     customer.save()
#     print(customer)
#     return render(request,'Agent/manage-customers.html',)


def product_in_store(request):
    table_data = {}
    Total = 0
    arrimg = []
    arrvalu = []
    arrkey = []

    if request.user.groups.all()[0].name == 'Agent':
        all_Product = Product.objects.all()
        user = User.objects.get(id=request.user.id)
        agent = Agent.objects.get(user=user)
        spesific_store_agent = Agent_Store.objects.get(agent=agent)

        product_amount = Product_Amount_in_Store_agent.objects.get(
            store=spesific_store_agent)

        refile_product = add_to_store_agent.objects.filter(
            Store=spesific_store_agent).order_by('-date_created')

        for product in all_Product:
            arrimg.append(product.img)
            table_data[product.Product_Name] = (
                (getattr(product_amount, product.Product_Name)))
            Total += getattr(product_amount, product.Product_Name)
        print(Total)
        for key, valu in table_data.items():
            arrkey.append(key)
            arrvalu.append(valu)
        num = []
        x = 0
        for i in refile_product:
            num.append(x)
            x = x+1
        data = zip(arrkey, arrvalu, arrimg)

        if request.method == 'POST':
            name = request.POST['product']
            print(name)
            old_amount = getattr(product_amount, name)
            print(old_amount)
            new_amount = request.POST['amount']
            print(new_amount)
            update_amount = old_amount + int(new_amount)
            print(update_amount)
            setattr(product_amount, name, update_amount)
            product_amount.save()
            add_to_store_agent.objects.create(
                Store=spesific_store_agent, product=name, qunitiy=new_amount)
            messages.info(request, 'Store refilled successfully')
            return redirect('product-in-store')

        context = {

            'all_Product': all_Product,
            'table_data': table_data,
            'Total': Total,
            'data': data,
            'company_manager': agent,
            'spesific_store': spesific_store_agent,
            'refile_product': refile_product,
            'num': num,
        }

    return render(request, 'Agent/product-in-agent-store.html', context)


def transaction_detail(request, pk):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            transaction = Agent_Transaction.objects.get(id=pk)
            products = Product.objects.all()
            order = Agent_order.objects.get(id=transaction.Agent_order_id.id)
            price = []
            prods = []
            quantity = []
            sub_total = []
            grand_total = 0
            VAT_Paid = 0.0
            total_quantity = 0
            for product in products:
                price.append(product.Price_in_creates)
                prods.append(product.Product_Name)
                quantity.append(getattr(order, product.Product_Name))
                sub_total.append(product.Price_in_creates *
                                 getattr(order, product.Product_Name))
                grand_total += float(product.Price_in_creates *
                                     getattr(order, product.Product_Name))
                total_quantity += (getattr(order, product.Product_Name))
                VAT_Paid = float(grand_total * 0.15)

            data = zip(prods, price, quantity, sub_total)

            context = {
                'transaction': transaction,
                'data': data,
                'total_quantity': total_quantity,
                'grand_total': grand_total,
                'VAT': VAT_Paid,

            }
            return render(request, 'Agent/transaction-details.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


# ////////////////////////////////////////////////////// Vichel Managemetn //////////////////////////

def add_vehicle(request):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            request_agent = Agent.objects.get(user=request.user)
            if request.method == 'POST':

                vichel_type = request.POST.get('car_type')
                vichel_name = request.POST.get('vehicle_name')
                vichel_No = request.POST.get('plate_num')
                vichel_pic = request.FILES.get('vehiclePhoto')
                print(vichel_pic)
                new = Vehicle.objects.create(
                    vichel_type=vichel_type, vichel_name=vichel_name, vichel_No=vichel_No, vichel_pic=vichel_pic, Agent=request_agent)
                if new:
                    messages.success(request, 'vihecle successfully added')
                    return redirect('manage_vehicles')
                else:
                    messages.error(
                        request, 'something went wrong. please, try again')
            return render(request, 'Agent/add-vehicle.html',)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def delete_vehicle(request, pk):
    try:
        if request.user.groups.all()[0].name == 'Agent':

            vihecle = Vehicle.objects.get(id=pk)
            agent = Agent.objects.get(user=request.user)
            if agent == vihecle.Agent:
                vihecle.delete()
                messages.success(request, 'Vihelce successfully deleted')
                return redirect('manage_vehicles')
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def manage_vehicles(request):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            agent = Agent.objects.get(user=request.user)
            all_vechil = Vehicle.objects.filter(Agent=agent)
            context = {
                'all_vechil': all_vechil,
            }
            return render(request, 'Agent/manage-vehicles.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


# ///////////////////////////////////////////////////// End Vichel /////////////////////////////////////


# ////////////////////////////////////////////////////// Driver Managemetn //////////////////////////
def add_driver(request):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            agent = Agent.objects.get(user=request.user)
            all_vechil = Vehicle.objects.filter(Agent=agent)
            context = {
                'all_vechil': all_vechil,
            }
            if request.method == 'POST':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                username = request.POST.get('username')
                email = request.POST.get('email')
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                salary = request.POST.get('salary')
                phone1 = request.POST.get('phone')
                vehicle = request.POST.get('vechile')
                assign_ = Vehicle.objects.get(vichel_No=vehicle)

                profile_pic = request.FILES.get('licence')
                Drive_license = request.FILES.get('photo')
                Full_name = first_name + ' ' + last_name
                if password1 == password2:
                    new = User.objects.filter(username=username)
                    new1 = User.objects.filter(email=email)
                    if new.count():
                        messages.error(
                            request, 'User in this username already exist')
                        return render(request, 'Agent/add-driver.html', context)
                    elif new1.count():
                        messages.error(
                            request, 'User in this email already exist')
                        return render(request, 'Agent/add-driver.html', context)
                    else:
                        user = User.objects.create(
                            first_name=first_name, last_name=last_name, email=email, username=username, password=password1)
                        my_group = Group.objects.get(name='Driver')
                        my_group.user_set.add(user)
                        driver = Driver.objects.create(Agent=agent, user=user, Full_name=Full_name, phone1=phone1,
                                                       vehicle=assign_, profile_pic=profile_pic, Drive_license=Drive_license, salary=salary)
                        if driver:
                            car_ststus = Vehicle.objects.get(vichel_No=vehicle)
                            car_ststus.status = True
                            car_ststus.save()
                            messages.success(
                                request, 'Driver successfully added')
                            return redirect('manage_drivers')
                        else:
                            messages.error(
                                request, 'something went wrong. please, try again')

                else:
                    messages.error(request, 'Password didn\'t match!')
                    return render(request, 'Agent/add-driver.html', context)

            return render(request, 'Agent/add-driver.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def manage_drivers(request):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            agent = Agent.objects.get(user=request.user)
            all_drive = Driver.objects.filter(Agent=agent)
            context = {
                'all_drive': all_drive,
            }
            return render(request, 'Agent/manage-drivers.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def view_drivers_profile(request, pk):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            agent = Agent.objects.get(user=request.user)
            drive = Driver.objects.get(Agent=agent, id=pk)
            all_vechil = Vehicle.objects.filter(Agent=agent)
            if request.method == 'POST':
                salary = request.POST.get('Salary')
                vichile = request.POST.get('vihecle')
                vehicle = Vehicle.objects.get(vichel_No=vichile)
                drive.salary = salary
                drive.vehicle = vehicle
                drive.save()
            context = {
                'drive': drive,
                'all_vechil': all_vechil,
            }
            return render(request, 'Agent/driver_profile.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def delete_drivers(request, pk):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            agent = Agent.objects.get(user=request.user)
            drive = Driver.objects.get(Agent=agent, id=pk)
            all_drive = Driver.objects.filter(Agent=agent)
            drive.delete()
            messages.success(request, 'Driver successfully removed')

            context = {
                'all_drive': all_drive,
            }
            return render(request, 'Agent/manage-drivers.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')
# ////////////////////////////////////////////////////// End Driver Managemetn //////////////////////////

# problem


def transactions(request):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            all_transaction = Agent_Transaction.objects.all().order_by('-date_created')
            context = {
                'all_transaction': all_transaction,
            }
            return render(request, 'Agent/transactions.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def send_message(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        to_email = request.POST.get('to_email', '')
        from_email = request.POST.get('to_email', '')
        if subject and message and to_email:
            try:
                send_mail(subject, message, [
                          'efremyohanis115@gamil.com'], ['efremyohanis116@gamil.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, 'Agent/send-message.html', {})
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return render(request, 'Agent/send-message.html', {})

    return render(request, 'Agent/send-message.html', {})


def cust_change_password(request, pk):
    try:
        if request.user.groups.all()[0].name == 'Agent':
            if request.method == 'POST':
                old_password = request.POST.get('password')
                customer = Customer.objects.get(id=pk)
                if customer.user.check_password(old_password):
                    new_password = request.POST.get('newpassword')
                    renew_password = request.POST.get('renewpassword')
                    if new_password == renew_password:
                        customer.user.set_password(new_password)
                        customer.user.save()
                        return HttpResponse('password changed ,successfully')
                    return HttpResponse('old password and new password are not the same')
                return HttpResponse('old password doestn\'t exixt in the system')
            return render(request, 'Agent/manage-customers.html')
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')


def draiver_page(request):
    user = User.objects.get(id=request.user.id)
    print(user)
    driver = Driver.objects.get(user=user)
    print(driver.phone1)
    agent_id = driver.Agent.id
    agent = Agent.objects.get(id=agent_id)
    all_customer = Customer.objects.filter(Agent=agent)
    all_order = []
    all_orders = []
    all_transaction = []
    for cust in all_customer:
        try:
            if Customer_order.objects.get(Customer=cust):
                all_order.append(Customer_order.objects.get(
                    Customer=cust, driver=driver))
        except Exception as e:
            continue
    for order in all_order:
        try:
            if Customer_Transaction.objects.get(Customer_order_id=order.id):
                all_orders.append(
                    Customer_order.objects.get(id=order.id))
                all_transaction.append(
                    Customer_Transaction.objects.get(Customer_order_id=order.id))
        except Exception as e:
            continue
    data = zip(all_orders, all_transaction)
    context = {

        'data': data,
    }

    return render(request, 'Agent/driver.html',context)

   

def cusomer_order_ditel_driver(request, pk):
    
    try:
        if request.user.groups.all()[0].name == 'Driver':
            driver = Driver.objects.get(user=request.user)
            agent = driver.Agent

            try:

                transaction = Customer_Transaction.objects.get(id=pk)
                print(transaction)

            except AttributeError as e:
                return ('customer_order')
            products = Product.objects.all()

            order = Customer_order.objects.get(
                id=transaction.Customer_order_id.id)

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
            data = zip(prods, quantity)
            context = {
                'transaction': transaction,
                'data': data,
                'total_quantity': total_quantity,

            }
            return render(request, 'Agent/driver_page.html', context)
        messages.error(request, 'permission denied ')
        return redirect('logout')
    except IndexError as e:
        messages.error(request, 'Login Before ')
        return redirect('logout')
