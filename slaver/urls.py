from django.urls import path
from . import views
urlpatterns = [
     path("check_in",views.ChechIn,name="checkin"),
     path("request_on",views.RequestOpen,name='RequestOn'),
     path("request_off",views.RequestClose,name="RequestOff"),
     path("change_temper",views.RequestUpdateTemper,name="changeTemper"),
     path("change_speed", views.RequestUpdateSpeed,name='ChangeSpeed'),
     path("request_fee",views.RequestFee,name ="Fee"),
     path("check_out",views.CheckOut,name="checkout")
        # path('mainmachine',)
]

