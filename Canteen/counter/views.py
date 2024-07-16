from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from Store import models as storeModel
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

# from django.contrib.auth.models import User


def OrderAssembler(shop_id, filters, by_notification = False,queryset = None):
    orders = []
    # [
    #     [Order,Customer, [(Product, Qtty), (Product, qty), (Product,qtyty)..] ],
    #     [Order,Customer, [(Product, Qtty), (Product, qty), (Product,qtyty)..] ],
    #     [Order,Customer, [(Product, Qtty), (Product, qty), (Product,qtyty)..] ],
    #     [Order,Customer, [(Product, Qtty), (Product, qty), (Product,qtyty)..] ],
    # ]
    
    if by_notification:
        pp = storeModel.Orders.objects.filter(is_notified=False, shop__id=shop_id)
    elif queryset is not None:
        pp = queryset
    else:
        pp = storeModel.Orders.get_orders_by_status(shop_id=shop_id, filters=filters).order_by("-time") if filters != "all" else storeModel.Orders.objects.filter(shop__id=shop_id).order_by("-time")
    
    for order in pp:
        order.is_notified=True
        order.save()

        order_array = [order, storeModel.Customer.objects.get(user = order.user)]
        products_info = json.loads( order.products_info )
        temp = []
        for pid,qtty in products_info.items():
            try:
                temp.append( (storeModel.Product.objects.get(id=pid), qtty,) )
            except:pass
        order_array.append(temp)
        orders.append(order_array)
    return orders

def Signout(request):
    logout(request)
    return redirect("counterhome")


def get_order_details(shop_id):
    today_order_count = storeModel.Orders.objects.filter(shop=shop_id, date=timezone.localdate()).count()
    pending_orders_count = storeModel.Orders.get_orders_by_status(shop_id=shop_id, filters="accepted").count()
    delivered_orders_count = storeModel.Orders.get_orders_by_status(shop_id=shop_id ,filters="completed").count()
    return today_order_count, pending_orders_count, delivered_orders_count


def home(request):
    if request.user.is_authenticated and request.user.is_staff:
        try:
            shop_details = storeModel.Shop.objects.get(owner=request.user)
        except:
            return HttpResponse("<h1>You are not authorized to access this page<h1>")
        # ? pending orders = accepted orders
        orders = OrderAssembler(shop_id=shop_details.id ,filters="active")
        
        today_order_count, pending_orders_count, delivered_orders_count = get_order_details(shop_details.id)
        return render(request, 'counter/home.html',
                    {
                        "orders":orders,
                        "shop_details":shop_details,
                        "pending_orders_count":pending_orders_count,
                        "delivered_orders_count":delivered_orders_count,
                        "today_order_count":today_order_count if today_order_count else 0,
                    }
        )
    return redirect(reverse("counterlogin", current_app="counter"))

def Completedrders(request):
    if request.user.is_authenticated and request.user.is_staff:

        try:
            shop_details = storeModel.Shop.objects.get(owner=request.user)
        except:
            return HttpResponse("<h1>You are not authorized to access this page<h1>")
        # ? pending orders = accepted orders
        
        orders = OrderAssembler(shop_id=shop_details.id ,filters="completed")
        today_order_count, pending_orders_count, delivered_orders_count = get_order_details(shop_details.id)

        return render(request, 'counter/completed.html',{
                "orders":orders, 
                "shop_details":shop_details,
                "delivered_orders_count":delivered_orders_count,
                "pending_orders_count":pending_orders_count,
                "today_order_count":today_order_count if today_order_count else 0,
            })
    else:
        return redirect(reverse("counterlogin", current_app="counter"))


def CounterManLogin(request):
    
    if request.method == "GET":
        if request.user.is_staff and request.user.is_authenticated:
            return redirect("counterhome")
        else:
            return render(request,"counter/login.html")
    else:
        email = request.POST.get('email')
        password = request.POST.get('psw')

        user = authenticate(username= email, password = password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect("counterhome")
        else:
            return render(request, 'counter/login.html', {"err":"Invalid username or password!!"})

def AllOrders(request):

    if request.user.is_authenticated and request.user.is_staff:
        orders = queryset =""
        
        try:
            shop_details = storeModel.Shop.objects.get(owner=request.user)
        except:
            return HttpResponse("<h1>You are not authorized to access this page<h1>")
        # ? pending orders = accepted orders
        
        today_order_count, pending_orders_count, delivered_orders_count = get_order_details(shop_details.id)

        if request.method == "POST":
            filtr = request.POST.get("all-page-filter")

            if filtr == "all":
                queryset = storeModel.Orders.objects.filter(shop=shop_details)
            elif filtr == "today":
                today = timezone.localdate()
                queryset = storeModel.Orders.objects.filter(date=today, shop=shop_details)
            elif filtr == "month":
                m = timezone.localdate().month
                queryset = storeModel.Orders.objects.filter(date__month=m, shop=shop_details)
            


            orders =  OrderAssembler(shop_id=shop_details.id ,filters="all", queryset = queryset)
            return render(request, 'counter/all.html',
                {
                    "orders":orders, 
                    "shop_details":shop_details,
                    "delivered_orders_count":delivered_orders_count,
                    "pending_orders_count":pending_orders_count,
                    "today_order_count":today_order_count if today_order_count else 0,
                })

        else:       
            orders = OrderAssembler(shop_id=shop_details.id ,filters="all")
            return render(request, 'counter/all.html',
                {
                    "orders":orders, 
                    "shop_details":shop_details,
                    "delivered_orders_count":delivered_orders_count,
                    "pending_orders_count":pending_orders_count,
                    "today_order_count":today_order_count if today_order_count else 0,
                })
    else:
        return redirect(reverse("counterlogin", current_app="counter"))


def FailedOrders(request):
    if request.user.is_authenticated and request.user.is_staff:
        
        try:
            shop_details = storeModel.Shop.objects.get(owner=request.user)
        except:
            return HttpResponse("<h1>You are not authorized to access this page<h1>")
        # ? pending orders = accepted orders
        
        orders = OrderAssembler(shop_id=shop_details.id ,filters="failed")
        today_order_count, pending_orders_count, delivered_orders_count = get_order_details(shop_details.id)

        return render(request, 'counter/failed.html',
            {
                "orders":orders, 
                "shop_details":shop_details,
                "delivered_orders_count":delivered_orders_count,
                "pending_orders_count":pending_orders_count,
                "today_order_count":today_order_count if today_order_count else 0,
            })
    else:
        return redirect(reverse("counterlogin", current_app="counter"))

def AcceptedOrder(request):
    if request.user.is_authenticated and request.user.is_staff:
        
        try:
            shop_details = storeModel.Shop.objects.get(owner=request.user)
        except:
            return HttpResponse("<h1>You are not authorized to access this page<h1>")
        # ? pending orders = accepted orders
        
        today_order_count, pending_orders_count, delivered_orders_count = get_order_details(shop_details.id)

        orders = OrderAssembler(shop_id=shop_details.id ,filters="accepted")
        return render(request, 'counter/accepted.html',{
                "orders":orders, 
                "shop_details":shop_details,
                "delivered_orders_count":delivered_orders_count,
                "pending_orders_count":pending_orders_count,
                "today_order_count":today_order_count if today_order_count else 0,
            })
    else:
        return redirect(reverse("counterlogin", current_app="counter"))

def RejectedOrder(request):
    if request.user.is_authenticated and request.user.is_staff:

        try:
            shop_details = storeModel.Shop.objects.get(owner=request.user)
        except:
            return HttpResponse("<h1>You are not authorized to access this page<h1>")
        # ? pending orders = accepted orders
        
        orders = OrderAssembler(shop_id=shop_details.id ,filters="rejected")
        today_order_count, pending_orders_count, delivered_orders_count = get_order_details(shop_details.id)

        return render(request, 'counter/rejected.html',{
                "orders":orders, 
                "shop_details":shop_details,
                "delivered_orders_count":delivered_orders_count,
                "pending_orders_count":pending_orders_count,
                "today_order_count":today_order_count if today_order_count else 0,
            })
    else:
        return redirect(reverse("counterlogin", current_app="counter"))

def SetOrderStatus(request, status, pid):
    if request.user.is_authenticated and request.user.is_staff:
            storeModel.Orders.objects.filter(id=pid).update(order_status=status)
            return redirect(request.META.get("HTTP_REFERER"))


def NotificationAJAX(request, sid):
    if request.user.is_authenticated and request.user.is_staff:
    # {name, number, address, amount, itemxqtty, status, payment, placed at}
        res = OrderAssembler(shop_id=sid ,filters='all', by_notification=True)

        if not res == []:
            data = []
            status = 'ok'
            for obj in res:
                temp = {}
                temp["id"] = obj[0].id
                temp["name"] = obj[1].user.first_name
                temp["number"] = obj[1].number
                temp["address"] = obj[1].address
                temp["amount"] = obj[0].amount
                temp["itemxqtty"] = ",".join( f"{product.name} x {qtty}" for product,qtty in obj[2] )
                temp["status"] = obj[0].order_status
                temp["txn_status"] = obj[0].txn_status
                # temp["placed_at"] = obj[0].time.strftime(r"%b. %d, %Y %I:%M, %p")
                temp["time"]  = obj[0].time,
                temp["date"] = obj[0].date,
                temp["payment_method"] = obj[0].payment_method,
                temp["order_id"] = obj[0].razorpay_order_id
                data.append(temp)
        else:
            status = "no"
            data = {}
        return JsonResponse({"status":status, "data": data}, safe=False, )
    else:
        return JsonResponse({"status":"NA", "data":"Chala jaa bsdka"})


def SetShopStatus(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":
            shop = storeModel.Shop.objects.filter(owner=request.user)[0]

            flag = request.POST.get("shop-status")
            if flag is not None and flag == "true":
                shop.is_open = True
            else:
                shop.is_open = False
            shop.save()
            return redirect(request.META.get('HTTP_REFERER'))


def ShopProducts(request):
    if request.user.is_authenticated and request.user.is_staff:

        try:
            shop_details = storeModel.Shop.objects.get(owner=request.user)
        except:
            return HttpResponse("<h1>You are not authorized to access this page<h1>")
        # ? pending orders = accepted orders
        
        products = storeModel.Product.objects.filter(shop=shop_details)
        today_order_count, pending_orders_count, delivered_orders_count = get_order_details(shop_details.id)

        return render(request, 'counter/products.html',{
                    "shop_details":shop_details,
                    "delivered_orders_count":delivered_orders_count,
                    "pending_orders_count":pending_orders_count,
                    "products":products,
                    "today_order_count":today_order_count if today_order_count else 0,
                })


def SetProductStatus(request, pid):
    if request.user.is_authenticated and request.user.is_staff:
        products = storeModel.Product.objects.get(id=pid)
        flag = request.POST.get("product-status")
        if flag is not None and flag == "true":
            products.availibility = True
        else:products.availibility = False

        products.save()
        return redirect(request.META.get('HTTP_REFERER'))
