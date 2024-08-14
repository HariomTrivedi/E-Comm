# shop/views.py
from rest_framework import generics
import paypalrestsdk
from django.conf import settings
from .models import Product, Contact, Orders, orderUpdate
from .serializers import ProductSerializer, ContactSerializer, OrdersSerializer, OrderUpdateSerializer
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Contact, Orders, orderUpdate
from math import ceil



class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ContactListCreate(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class OrdersListCreate(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

class OrderUpdateListCreate(generics.ListCreateAPIView):
    queryset = orderUpdate.objects.all()
    serializer_class = OrderUpdateSerializer


# Create your views here.

# Configure PayPal SDK
# paypalrestsdk.configure({
#     "mode": settings.PAYPAL_MODE,  # sandbox or live
#     "client_id": settings.PAYPAL_CLIENT_ID,
#     "client_secret": settings.PAYPAL_CLIENT_SECRET
# })

def index(request):
    # products = Product.objects.all()
    # print(products)
    #n = len(prod)
    # nSlides = n//4 + ceil((n/4))-((n//4))
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4)) - (n // 4)
        allProds.append([prod, range(1, nSlides + 1), nSlides])

    # data = {
    #    'no_of_slides':nSlides, 'range':range(nSlides,), 'product' : products
    # }
    # allProds = [[products,range(1, len(products)),nSlides],
    #          [products,range(1, len(products)),nSlides],]
    data = {
        'allProds': allProds
    }
    return render(request, 'shop/index.html', data)
def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False
def search(request):
    query = request.GET.get('search')
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item) ]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4)) - (n // 4)
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides + 1), nSlides])
    data = {
        'allProds': allProds, "msg": ""
    }
    if len(allProds) == 0 or len(query)<4:
        data = {"msg": "Search result not exist"}
    return render(request, 'shop/search.html', data)

    

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name','')
        email= request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
    return render(request,'shop/contact.html')

def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if order.exists():
                updates = orderUpdate.objects.filter(order_id=orderId)
                updates_list = [{'text': item.update_desc, 'time': item.timestamp} for item in updates]
                items_json = json.loads(order[0].items_json)  # Ensure this is valid JSON
                response_data = json.dumps([updates_list, items_json], default=str)
                return HttpResponse(response_data, content_type='application/json')
            else:
                return HttpResponse(json.dumps([]), content_type='application/json')
        except Exception as e:
            return HttpResponse(json.dumps([]), content_type='application/json')
    return render(request, 'shop/tracker.html')


def productView(request,myid):
    #featch the product using id
    product = Product.objects.filter(id = myid)
    return render(request,'shop/prodView.html', {'product':product[0]})

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')

        order = Orders(
            items_json=items_json, name=name, email=email, address=address,
            city=city, state=state, zip_code=zip_code, phone=phone,
        )
        order.save()

        # Add order update
        update = orderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'shop/checkout.html')
