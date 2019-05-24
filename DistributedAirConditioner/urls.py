from django.contrib import admin
from django.urls import path
from Logger import views as logger_views
from Statistic import views as statistic_views 





urlpatterns = [
    path('admin/', admin.site.urls),
    path('logger/query_report', logger_views.LoggerQueryReport),
    path('logger/print_report', logger_views.LoggerPrintReport),
    path('logger/query_invoice', logger_views.LoggerQueryInvoice),
    path('logger/print_invoice', logger_views.LoggerPrintInvoice),
    path('logger/query_rdr', logger_views.LoggerQueryRdr),
    path('logger/print_rdr', logger_views.LoggerPrintRdr),
    path('test/', logger_views.test),
]
