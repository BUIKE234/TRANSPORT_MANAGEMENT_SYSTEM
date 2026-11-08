from django.urls import path
from . import views

urlpatterns =[
    path('',views.login_view,name='landing'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('receipt/<int:trip_id>/', views.receipt_view, name='receipt'),
    path('report/',views.report_view,name='report')
]