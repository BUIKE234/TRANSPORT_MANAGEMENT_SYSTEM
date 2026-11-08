from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from transport.models import Truck, Driver, Trip, Payment

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username= request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'only Admin can login. Use your superuser account')
    return render(request, 'login.html')     

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    total_trucks = Truck.objects.count()
    total_drivers=Driver.objects.count()
    total_trips=Trip.objects.count()
    total_charges = Trip.objects.aggregate(total=Sum('TransportCharge'))['total'] or 0
    total_paid= Payment.objects.aggregate(total=Sum('AmountPaid'))['total'] or 0
    total_outstanding = sum(trip.BalanceToPay for trip in Trip.objects.all())
    recent_trips= Trip.objects.order_by('-id')[:10]
    recent_payments = Payment.objects.select_related('Trip', 'Trip__truck', 'Trip__Driver').order_by('-id')[:10]
    context ={
        "total_trucks":total_trucks,
        "total_drivers":total_drivers,
        "total_trips":total_trips,
        "total_charges":total_charges,
        "total_paid":total_paid,
        "total_outstanding":total_outstanding,
        "recent_trips": recent_trips,
        "recent_payments": recent_payments,
    }
    return render(request,'dashboard.html',context)

@login_required
def receipt_view(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    payments = trip.payments.all().order_by('-id')
    total_paid = sum(payment.AmountPaid or 0 for payment in payments)
    context = {
        'trip': trip,
        'payments': payments,
        'total_paid': total_paid,
        'balance_to_pay': trip.BalanceToPay,
    }
    return render(request, 'receipt.html', context)

@login_required
def report_view(request):
    Trips =Trip.objects.all().order_by('-id') 
    total_charges = Trip.objects.aggregate(total=Sum('TransportCharge'))['total'] or 0   
    total_paid = Payment.objects.aggregate(total=Sum('AmountPaid'))['total'] or 0
    total_outstanding = sum(trip.BalanceToPay for trip in Trip.objects.all())
    context ={
        'trips': Trips,
        'total_charges':total_charges,
        'total_paid':total_paid,
        'total_outstanding': total_outstanding
    }
    return render(request, 'report.html', context)