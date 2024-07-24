
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name="homepage"),
    path('search/', views.get_search_results, name=""),
    path('refreshment/<int:pid>/', views.ProductView.as_view(), name=""),
    path('post-review/<int:pid>/', views.ProductFeedback.as_view(), name=""),
    path('profile/', views.ProfilePage.as_view(), name="userprofile"),
    path('about/', views.AboutPage, name="aboutpage"),
    path('login/', views.LoginPage.as_view(),name="loginpage"),
    path('register/', views.RegisterUser.as_view()),
    path('logout/', views.Signout),
    path('cart/', views.CartPage, name="cartpage"),
    path('orders/', views.UserOrders),
    path('payment/', views.Payment.as_view()),
    path('order-success/<int:orderId>/', views.OrderSuccess, name="ordersuccess"),
    path('handlepayment/', views.paymenthandler),
    path('terms-and-conditions/', views.tc),
    path('set-cart/<str:action>/', views.ManageSessionCart),
]

