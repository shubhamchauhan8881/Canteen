import razorpay
from . import forms
from . import models
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,HttpResponseBadRequest, JsonResponse, HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required
import json
from django.conf import settings
import razorpay
import string
import random
from django.contrib import messages


from asgiref.sync import sync_to_async
from . import sendMessage

deliveryCharge =0
MIN_AMOUT_ORDER = 40


def Signout(request):
    logout(request)
    return redirect("homepage")
# Create your views here.


class HomePage(View):
    def get(self, request):
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
        
        # filters
        shop_id = request.GET.get("shop")
        restaurents = models.Shop.objects.all()

        if shop_id is not None:
            category = models.Category.objects.filter(shop=restaurents.filter(id=shop_id)[0])
            product = models.Product.objects.filter(visibility=True, shop=restaurents.filter(id=shop_id)[0])
        
            data = self.getProducts(category, restaurents.filter(id=shop_id), product)

        else:
            category = models.Category.objects.all()
            product = models.Product.objects.filter(visibility=True)
            data = self.getProducts(category, restaurents, product)
        return render(request, "store/Homepage.html", {"data":data, "restaurents":restaurents,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})

    def getProducts(self,category, shop, product):
        res = []
        for restaurent in shop:
            temp = []
            c = category.filter(shop=restaurent)
            for i in c:
                p = product.filter(shop=restaurent, product_ctgry=i)
                temp.append( (i, p) )
            res.append( (restaurent, temp) )
        return res

# [
#     ("Khare kitchen", [ ("Category",<QuerySet>) ..  ]  )
# ]



@csrf_exempt
def get_search_results(request):
    name = request.POST.get("input")
    
    #fetch products
    products = models.Product.objects.filter(name__icontains=name)
    if products.count() <= 0:
        return JsonResponse({"ok":True, "message":f"No matching products for {name}"}, status=404)
    else:
        d = [{"id":p.id, "name":p.name} for p in products]
        return JsonResponse({"ok":True, "data":d}, status=200)



class ProfilePage(View):
    def get(self, request):
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
        if request.user.is_authenticated:
            c = models.Customer.objects.get(user__id = request.user.id)
            editForm = forms.UserEditForm(data={"email":request.user.username,"name":request.user.first_name, "phone":c.number, "address":c.address})
            return render(request, "store/profile.html", {"editForm":editForm,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})
        else:return redirect("loginpage")

    def post(self, request):
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
        if request.user.is_authenticated:

            form = forms.UserEditForm(data=request.POST)
            if form.is_valid():
                User.objects.filter(username=request.user.username).update(
                    first_name= form.cleaned_data["name"]
                )
                models.Customer.objects.filter(user__id = request.user.id).update(
                    number=form.cleaned_data["phone"],
                    address=form.cleaned_data["address"],
                )
                messages.success(request,"Details updated successfully!")
                return render(request, "store/profile.html", {"editForm":form,"profileUpdated":True, "NEW_IN_THE_MENU":NEW_IN_THE_MENU})
            else:
                return render(request, "store/profile.html", {"editForm":form, "NEW_IN_THE_MENU":NEW_IN_THE_MENU})
        else:return redirect("loginpage")




class ProductView(View):
    def get(self, request, pid):
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
        category = models.Category.objects.all()
        restaurents = models.Shop.objects.all()

        p = models.Product.objects.get(id=pid)
        more = models.Product.objects.filter(shop=p.shop, availibility= True, visibility=True).exclude(id=p.id)

        review = models.ProductReviews.objects.filter(product=p, approved=True)
        return render(request, "store/product-view.html", {"product":p,"reviews":review,"restaurents":restaurents,"categories":category, "more":more,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})



class ProductFeedback(View):
    def get(self, request, pid):
        review = models.ProductReviews.objects.create(
            user=request.user if request.user.is_authenticated else None,
            product=models.Product.objects.get(id=pid),
            review=request.GET.get('feedback'),
        )
        messages.success(request, "Thank you for your feedback! Your review has been recorded and is currently under review. Once verified, it will be publicly visible.")
        return redirect(request.META.get('HTTP_REFERER'), permanent=True)


class LoginPage(View):
    def get(self, request):
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
        loginForm = forms.LoginForm()
        return render(request, "store/login.html", {"loginForm":loginForm,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})

    def post(self, request):
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("homepage")
        # print(form.errors)
        form.add_error("password", "Invalid email and/or password.")
        return render(request, "store/login.html", {"loginForm":form,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})


class RegisterUser(View):
    def get(self, request):
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
        registerForm = forms.RegisterForm()
        return render(request, "store/register.html", {"registerForm":registerForm,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})

    def post(self, request):
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
        regForm = forms.RegisterForm(request.POST)
        if regForm.is_valid():
            user = User.objects.create(
                username= regForm.cleaned_data["email"],
                first_name= regForm.cleaned_data["name"],
                email= regForm.cleaned_data["email"],
            )
            user.set_password(regForm.cleaned_data["password"])
            user.save()
            customer = models.Customer.objects.create(
                user= user,
                number=regForm.cleaned_data["phone"],
                address= regForm.cleaned_data["address"]
            )

            login(request, user)
            return redirect("homepage")

        else:return render(request, "store/register.html", {"registerForm":regForm,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})



def tc(request):
    NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
    return render(request, "store/tc.html", {"NEW_IN_THE_MENU":NEW_IN_THE_MENU})

@login_required
def CartPage(request):
    NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
    # if request.method == "POST":
    products = []
    total = deliveryCharge
    cant_place_order = False
    shop_diff = False
    try:
        cartItems = request.GET.get("cartInput")
        shops = {}
        for pid, qtty in  json.loads(cartItems).items():
            p = models.Product.objects.get(id=int(pid))
            
            if not p.shop.is_open:
                messages.error(request,f"{p.shop.name} is closed for now! Unable to plcae order.")
                return redirect(request.META.get("HTTP_REFERER"))

            elif shops.get(p.shop) is not None:
                shops[p.shop] += 1
            else:
                shops[p.shop] = 1
            
            products.append((p,qtty))
            total += (p.price*qtty)
        request.session["payment"] = cartItems

        customer = models.Customer.objects.get(user__id=request.user.id)

        err_message = ""
        if total < MIN_AMOUT_ORDER:
            cant_place_order = True
            err_message =f"To serve you better, a minimum order amount of Rs. {MIN_AMOUT_ORDER} is required. Happy shopping!"

        if len(shops) > 1:
            cant_place_order = True
            err_message = f"Order from two different canteens can not be placed at the same time i.e., "+ ", ".join([x.name for x in shops.keys()]) + ". If you still want to place order, please place different orders for each. Thank you!"
            
        if cant_place_order:
            messages.error(request, err_message)

        return render(request, "store/cart.html", {"products":products,"err_message":err_message, "deliveryCharge":deliveryCharge,"MIN_ORDER_AMOUNT":MIN_AMOUT_ORDER,"cant_place_order":cant_place_order,"total":total,"customer":customer,"NEW_IN_THE_MENU":NEW_IN_THE_MENU})
    except:
        return render(request, "store/cart.html", {"cartEmpty":True,  "NEW_IN_THE_MENU":NEW_IN_THE_MENU})





def OrderSuccess(request, orderId):
    # p  = []
    try:
        order = models.Orders.objects.get(id=orderId, user=request.user)
        NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
        address = request.user.first_name +", " + order.againPhone + ", " + order.againAddress

        # for pid, qtty in json.loads(order.products_info):
        #     p = 
        #     p.appe()
    except:
        messages.error(request,"We faced an error while results.")
    return render(request, "store/paymentsuccess.html", {"order":order,"address":address,'NEW_IN_THE_MENU':NEW_IN_THE_MENU})



class Payment(View):
    def post(self, request):
        
        againPhone = request.POST["againPhone"]
        againAddress = request.POST["againAddress"]
        paymentmethod = request.POST["paymentmethod"]

        customer = models.Customer.objects.get(user=request.user)
        if againAddress == "":
            againAddress = customer.address
        if againPhone == "":
            againPhone = customer.number


        # product info
        amount = deliveryCharge
        item_x_quantity = ""
        cartItems = request.session["payment"]

        for pid, qtty in  json.loads(cartItems).items():
            p = models.Product.objects.get(id=int(pid))
            amount += (p.price*qtty)
            item_x_quantity += f"{p.name} x {p.price}, "

        if amount < MIN_AMOUT_ORDER:
            messages.error(request,f"Minimum order value is {MIN_AMOUT_ORDER}")
            return redirect(to="cartpage", permanent=True)


        order_id = 'CS' + "".join(random.sample(['0','1','2','3','4','5','6','7','8','9', *string.ascii_letters], 10))

        order = models.Orders.objects.create(
            shop=p.shop,
            user = request.user,
            products_info =cartItems,
            againPhone= againPhone,
            againAddress= againAddress,
            amount=amount,
        )

        if paymentmethod == "cod":
            order.txn_status = "complete"
            order.razorpay_order_id = order_id
            order.order_status="active"
            order.save()

            # send notification to restaurant
            clients = [client.client_id for client in models.TelegramClients.objects.filter(shop=order.shop)]

            Notificationdata = (
                order.razorpay_order_id,
                item_x_quantity,
                customer.user.get_full_name(),
                customer.number,
                customer.address,
            )
            sendMessage.send(data=Notificationdata,to=clients)

            order_details = {
                "name": request.user.first_name,
                "number": customer.number if customer.number else againPhone,
                "address": customer.address if customer.address else againAddress,
                "amount":amount,
                "item_x_quantity": item_x_quantity,
                "status": order.order_status,
                "payment": order.txn_status ,
                "placed_at": order.time.strftime(r"%b. %d, %Y, %I:%M %p"),
                "order_id": order.id,
            }
            return HttpResponsePermanentRedirect(f"/order-success/{order.id}")

        else:
            NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()

            client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
            data = {"amount": amount*100, "currency": "INR", "receipt": order_id}
            razor_order  = client.order.create(data=data)
            razor_order_id = razor_order["id"]
            razor_order_reciept = razor_order["receipt"]

            payment = {
                "keyid":settings.KEY_ID,
                "id": razor_order_id,
                "shopname":"Cravies",
                "currency":"INR",
                "amount":amount*100,
                "url":"/handlepayment/",
                "name":customer.user.first_name,
                "email":customer.user.email,
                "number":customer.number,
            }

            order.razorpay_order_id= razor_order_id
            order.razorpay_order_reciept= razor_order_reciept
            order.payment_method = "online"
            order.save()
            return render(request, "store/payment_processing.html",{"payment":payment, "NEW_IN_THE_MENU":NEW_IN_THE_MENU})

@csrf_exempt
def paymenthandler(request):
    NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            razorpay_client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                order = models.Orders.objects.filter(razorpay_order_id=razorpay_order_id).update(
                    txn_status='paid',
                    order_status="active",
                    razorpay_signature=signature,
                    razorpay_payment_id=payment_id
                )
                # c = models.Customer.objects.get(user__id=request.user.id)
                # address = request.user.first_name +", " + c.number +", " + c.address
                # return render(request, 'store/paymentsuccess.html',{"orderid":razorpay_order_id,"transactionid":payment_id, "address":address, "NEW_IN_THE_MENU":NEW_IN_THE_MENU})
            
                request.session["order_id"] = order.id
                return redirect('ordersuccess', permanent=True)
            
            else:
                models.Orders.objects.filter(razorpay_order_id=razorpay_order_id).update(
                    txn_status='failed',
                    razorpay_signature=signature,
                    razorpay_payment_id=payment_id
                )
                return render(request, 'store/paymentfail.html',{"orderid":razorpay_order_id, "NEW_IN_THE_MENU":NEW_IN_THE_MENU})
        except Exception as e:
            print(e)
            return render(request, 'store/orderfailed.html',{"orderid":razorpay_order_id, "NEW_IN_THE_MENU":NEW_IN_THE_MENU})




def AboutPage(request):
    NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
    return render(request, "store/about.html", {"NEW_IN_THE_MENU":NEW_IN_THE_MENU})

@csrf_exempt
def ManageSessionCart(request, action):
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False, "message": "Please login first."})
    
    pid = request.POST.get("pid")
    
    cart = models.Cart.get_by_pk(request.user, pid)

    if cart:
        if action == "add":
            cart.qtty += 1
        else:
            cart.qtty -= 1
            if cart.qtty <= 0:
                cart.delete()
                JsonResponse({"ok": True, "message": "cart item deleted", "new_qtty": 0})
        cart.save()
    else:
        cart = models.Cart.objects.create(
            user = request.user,
            product= models.Product.objects.get(pk=pid),
            qtty=1
        )

    return JsonResponse({"ok": True, "message": "chanegs updated", "new_qtty": cart.qtty})
    


@login_required(redirect_field_name="loginpage")
def UserOrders(request):
    NEW_IN_THE_MENU = models.NewInTheMenu.objects.all()[0].name.all()
    if request.method == "GET":
        user_orders = []
        o = models.Orders.objects.filter(user__id  = request.user.id).order_by("-time")
        for order in o:
            temp = [order, ]
            o_array = []
            for pid,qtty in json.loads(order.products_info).items():
                p = models.Product.objects.get(id=pid)
                o_array.append( ( p, qtty) )
            temp.append(o_array)
            user_orders.append(temp)
            # temp.extend([order,])
        return render(request, 'store/orders.html', {"orders":user_orders, "NEW_IN_THE_MENU":NEW_IN_THE_MENU})
