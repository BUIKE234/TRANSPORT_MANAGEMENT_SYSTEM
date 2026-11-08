from datetime import date, datetime, time

from django.db import models
from django.utils.dateparse import parse_datetime

class Truck(models.Model):
    plate_number = models.CharField(max_length=20, unique=True)
    truck_type = models.CharField(max_length=50)
    capacity=models.CharField(max_length=50, help_text="e.g 30 Tons")
    status = models.CharField(max_length=20, choices=[
        ('Available', 'Available'),
        ('On Trip', 'On Trip'),
        ('Maintenance', 'Maintenance'),
    ], default='Available')
    def __str__(self):
        return self.plate_number
class Driver(models.Model):
    FullName = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=20)
    LicenceNumber= models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.FullName
class Trip(models.Model):
    date = models.DateField(auto_now_add=True)
    CompanyName=models.CharField(max_length=100, default="Nasiru Transport")
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    Driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    FromLocation = models.CharField(max_length=100)
    ToLocation = models.CharField(max_length=100)
    goods = models.CharField(max_length=100)
    QuantityLoaded=models.DecimalField(max_digits=10, decimal_places=2)
    QuantityDelivered= models.DecimalField(max_digits=10,decimal_places=2)
    damage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Shortage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    TransportCharge= models.DecimalField(max_digits=12, decimal_places=2)
    AdvancedPayment=models.DecimalField(max_digits=10, decimal_places=2,default=0)

    @property
    def BalanceToPay(self):
        charge = self.TransportCharge or 0
        advance = self.AdvancedPayment or 0
        total_paid = sum(p.AmountPaid or 0 for p in self.payments.all())
        return charge - advance - total_paid

    @property
    def outstanding(self):
        return self.BalanceToPay

    def __str__(self):
        return f"{self.truck} - {self.FromLocation} to {self.ToLocation}"

class Payment(models.Model):
    Trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='payments')
    CompanyName=models.CharField(max_length=100, default="Nasiru Transport")
    AmountPaid = models.DecimalField(max_digits=12, decimal_places=2)
    AdvancedPayment=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    PaymentMethod=models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('Transfer', 'Transfer'),
        ('Bank', 'Bank'),

    ], default='Cash')
    PaymentDate= models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @property
    def payment_datetime(self):
        value = self.PaymentDate
        if value in (None, '', 'NULL'):
            return None
        if isinstance(value, datetime):
            if value.time() == time(0, 0, 0):
                return None
            return value
        if isinstance(value, date):
            return None
        if isinstance(value, str):
            cleaned = value.strip()
            if not cleaned:
                return None
            try:
                parsed = parse_datetime(cleaned)
                if isinstance(parsed, datetime):
                    if parsed.time() == time(0, 0, 0):
                        return None
                    return parsed
            except (TypeError, ValueError):
                pass
            try:
                dt = datetime.fromisoformat(cleaned)
                if dt.time() == time(0, 0, 0):
                    return None
                return dt
            except (TypeError, ValueError):
                try:
                    return datetime.strptime(cleaned, '%Y-%m-%d')
                except (TypeError, ValueError):
                    return None
        return None

    @property
    def BalanceToPay(self):
        if not self.Trip_id:
            return 0
        trip = self.Trip
        charge = trip.TransportCharge or 0
        advance = trip.AdvancedPayment or 0
        total_paid = sum(p.AmountPaid or 0 for p in trip.payments.all())
        return advance - total_paid

    def __str__(self):
        return f"₦{self.AmountPaid} for {self.Trip}"
    