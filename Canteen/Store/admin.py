from django.contrib import admin
from . import models
import json

from django.contrib.auth.models import User
# Register your models here.

class OrdersAdmin(admin.ModelAdmin):
    list_display = ["Order_id","shop","Items","Customer_name","Phone","Address","date","amount","payment_method", "txn_status", "order_status"]
    readonly_fields = ["time","date","razorpay_order_id","razorpay_order_reciept","razorpay_payment_id","razorpay_signature", "products_info"]
        
    def Order_id(self, obj):
        return obj.razorpay_order_id
    
    def Items(self, obj):
        s = ""
        for pid, qtty in  json.loads(obj.products_info).items():
            p = models.Product.objects.get(id=int(pid))
            s += f"{p.name} x {qtty},"
        return s
    
    def Customer_name(self, obj):
        return obj.user.first_name
    
    def Phone(self, obj):
        if obj.againPhone:
            return obj.againPhone
        else:
            phone = models.Customer.objects.get(user__id = obj.user.id).number
            return phone

    def Address(self, obj):
        if obj.againAddress:
            return obj.againAddress
        else:
            ad = models.Customer.objects.get(user__id = obj.user.id).address
            return ad
    

class NewInTheMenuAdmin(admin.ModelAdmin):
    list_display = ["Items"]

    def Items(self, obj):
        s = ""
        for i in obj.name.all():
            s += i.name + ", "
        return s

admin.site.register(models.Category)
admin.site.register(models.Shop)
admin.site.register(models.TelegramClients)
admin.site.register(models.Product)
admin.site.register(models.ProductReviews)
admin.site.register(models.Customer)
admin.site.register(models.NewInTheMenu, NewInTheMenuAdmin)
admin.site.register(models.Orders, OrdersAdmin)
# models.Cart