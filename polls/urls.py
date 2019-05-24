from django.urls import path
from . import views
#from . import mainmachine
urlpatterns = [
        path('',views.index,name='index'),
        path("insert",views.insert,name='insert')
      #  path('mainmachine',)
]