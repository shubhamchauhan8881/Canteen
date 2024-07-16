
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="counterhome"),
    path('logout/', views.Signout),
    path('login/', views.CounterManLogin, name="counterlogin"),
    path('all/', views.AllOrders),
    path('completed/', views.Completedrders),
    path('failed/', views.FailedOrders),
    path('accepted/', views.AcceptedOrder),
    path('rejected/', views.RejectedOrder),
    path('order/setstatus/<str:status>/<int:pid>/', views.SetOrderStatus),
    path('notification/<int:sid>/', views.NotificationAJAX),
    path('shop/products/', views.ShopProducts),
    path('set-shop-status/', views.SetShopStatus),
    path('set-product-status/<int:pid>/', views.SetProductStatus),
]
