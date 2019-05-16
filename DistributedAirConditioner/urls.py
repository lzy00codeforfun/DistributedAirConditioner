from django.contrib import admin
from django.urls import path
from Logger import views as logger_views
from Statistic import views as statistic_views 


def test(request):
	return render(request, "test.html")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logger/', logger_views.controller),
    path('test/', test),

    #path('statistic/', views.controller),
]
