from django.urls import path
from . import views
urlpatterns = [
        #path('',views.index,name='index'),

        path("power_on",views.openMainMachine,name='open'),
        path("init_param",views.init_param,name="init_param"),
        path("get_default",views.get_default_url,name="get_default"),
        path("start_up",views.StartUp,name="start_up"),
        path("close",views.Close,name="close"),
        path("check_room_state",views.check_room_state,name='checkroomstatus')
        #  path('mainmachine',)
]

