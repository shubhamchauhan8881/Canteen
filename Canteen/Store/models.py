from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files import File
# Create your models here.

class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='uploads/shop/images/', null=True, blank=True)

    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    is_open = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        new_image = self.reduce_image_size(self.image)
        self.image = new_image
        super().save(*args, **kwargs)

    def reduce_image_size(self, image):
        img = Image.open(image)
        thumb_io = BytesIO()
        img.save(thumb_io, "jpeg", quality=50)
        new_image = File(thumb_io, name=image.name)
        return new_image

    def __str__(self):
        return self.name



class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=12)
    address = models.CharField(max_length=300, default='', null=True, unique=False)
    alternate_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name



class Category(models.Model):
    name = models.CharField(max_length=20)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.shop.name +" "+ self.name


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    product_ctgry = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(blank=True, max_length=300)
    image = models.ImageField(upload_to="uploads/products/")
    offer_discounts = models.IntegerField(default=0)
    availibility = models.BooleanField(default=True)

    last_modified = models.DateTimeField(auto_now_add=True)
    # set to false if any products is no more sold... this help to maintian users purchase history
    visibility = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        new_image = self.reduce_image_size(self.image)
        self.image = new_image
        super().save(*args, **kwargs)
    
    def reduce_image_size(self, image):
        img = Image.open(image)
        thumb_io = BytesIO()
        img.save(thumb_io, "jpeg", quality=50)
        new_image = File(thumb_io, name=image.name)
        return new_image

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qtty = models.IntegerField(default=1)
    date_time_added = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_by_pk(user, pk):
        try:
            return Cart.objects.get(user=user, product__pk= pk )
        except:
            return False



class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products_info = models.CharField(max_length=1000, null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, blank=True)

    payment_method = models.CharField(max_length=200, default='cod')
    txn_status = models.CharField( max_length=20, default='unpaid')
    order_status = models.CharField( max_length=20, default='pending')

    againPhone = models.CharField(max_length=12)
    againAddress = models.CharField(max_length=300)

    amount = models.IntegerField(default=0)

    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    last_modified = models.DateTimeField(auto_now_add=True)

    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_order_reciept = models.CharField(max_length=100, null=True, blank=True)
    
    razorpay_payment_id  = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=800, null=True, blank=True)


    # for notification purposes....
    is_notified = models.BooleanField(default=False)

    def __str__(self):
        return self.razorpay_order_id

    @staticmethod
    def get_orders_by_status(shop_id,filters="pending"):
        return Orders.objects.filter(order_status=filters, shop__id=shop_id)


class NewInTheMenu(models.Model):
    name = models.ManyToManyField(to=Product)

    def __str__(self):
        return "NEW"


class TelegramClients(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    client_id = models.CharField(max_length=50)
    def __str__(self):
        return self.name +" " + self.client_id


class ProductReviews(models.Model):
    careted_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    review = models.CharField(max_length=500)
    no_of_stars = models.IntegerField(default=0)

    review_type = models.CharField(max_length=100, default="positive")

    approved = models.BooleanField(default=False)


    def __str__(self):
        return self.review[:10]
