# shop/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("productview/<int:myid>", views.productView, name="ProductView"),
    # path("checkout/", views.checkout, name="Checkout"),
    path('shop/checkout/', views.checkout, name='checkout'),

    # API endpoints
    path("api/products/", views.ProductListCreate.as_view(), name="product-list-create"),
    path("api/contacts/", views.ContactListCreate.as_view(), name="contact-list-create"),
    path("api/orders/", views.OrdersListCreate.as_view(), name="orders-list-create"),
    path("api/orderupdates/", views.OrderUpdateListCreate.as_view(), name="orderupdates-list-create"),
]
