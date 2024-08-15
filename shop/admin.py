from django.contrib import admin
from django.http import HttpResponse
from .models import Product, Contact, Orders, orderUpdate
import csv 

# Register your models here.

def export_orders_csv(modeladmin, request, queryset):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Items', 'Name', 'Email', 'Address', 'City', 'State', 'Phone', 'Zip Code'])

    # Write data rows.
    for order in queryset:
        writer.writerow([order.order_id, order.items_json, order.name, order.email, order.address, order.city, order.state, order.phone, order.zip_code])
    
    return response

export_orders_csv.short_description = "Export Selected Orders as CSV"

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'name', 'email', 'city', 'state', 'phone')
    actions = [export_orders_csv]

admin.site.register(Product)
admin.site.register(Contact)
# admin.site.register(Orders)
admin.site.register(orderUpdate)

