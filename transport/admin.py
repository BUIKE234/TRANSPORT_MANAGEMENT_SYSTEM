from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Truck, Driver,Trip,Payment

class NasiruAdminSite(AdminSite):
    site_header = "Nasiru Abubakar and sons nig LTD"
    site_title = "Nasiru Abubakar Admin page"
    index_title = "Welcome to Nasiru Abubakar and sons Transport management system"
    site_url = "/dashboard"

custom_admin_site = NasiruAdminSite(name='nasiru_admin')
custom_admin_site.site_header = "Nasiru Abubakar and sons nig LTD"
custom_admin_site.site_title = "Nasiru Abubakar Admin page"
custom_admin_site.index_title = "Welcome to Nasiru Abubakar and sons Transport management system"

admin.site.site_header = "Nasiru Abubakar and sons nig LTD"
admin.site.site_title = "Nasiru Abubakar Admin page"
admin.site.index_title = "Welcome to Nasiru Abubakar and sons Transport management system"

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1
    fields = ['AmountPaid','PaymentMethod', 'PaymentDate']
    readonly_fields=['PaymentDate']
@admin.register(Truck,site=custom_admin_site)
class TruckAdmin(admin.ModelAdmin):
    list_display=['plate_number','truck_type','capacity','status']
    list_filter=['status','truck_type']
    search_fields=['plate_number','truck_type']
    list_editable=['status']
    list_per_page=10
@admin.register(Driver,site=custom_admin_site)
class DriverAdmin(admin.ModelAdmin):
    list_display=['FullName','PhoneNumber','LicenceNumber']
    search_fields=['FullName','LicenceNumber','PhoneNumber']
    list_per_page=10    

@admin.register(Trip,site=custom_admin_site)
class TripAdmin(admin.ModelAdmin):
    list_display=['date','truck','Driver','FromLocation','ToLocation','goods','TransportCharge', 'balance_to_pay_display']
    list_filter=['date','truck','Driver']
    search_fields=['FromLocation','ToLocation','goods','truck__plate_number']
    date_hierarchy='date'
    inlines=[PaymentInline]

    def balance_to_pay_display(self, obj):
        return f"₦{obj.BalanceToPay}"
    balance_to_pay_display.short_description = "Balance to Pay"

@admin.register(Payment, site=custom_admin_site)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['Trip','AmountPaid','AdvancedPayment','BalanceToPay','PaymentMethod','payment_datetime_display']
    list_filter=['PaymentMethod']
    readonly_fields=['BalanceToPay']

    def payment_datetime_display(self, obj):
        if obj.payment_datetime is None:
            return '-'
        return obj.payment_datetime.strftime('%d %b %Y %H:%M:%S')
    payment_datetime_display.short_description = 'Payment Date'

    def has_view_permission(self, request, obj=None):
        return request.user.is_active

    def has_change_permission(self, request, obj=None):
        return bool(request.user.is_superuser)

    def has_delete_permission(self, request, obj=None):
        return bool(request.user.is_superuser)

