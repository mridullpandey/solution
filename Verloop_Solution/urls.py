from django.contrib import admin
from django.urls import path,include
from gelocation import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/',include('rest_framework.urls')),
    path('getAddressDetails',views.Location.as_view(),name='temp'),
    path('',views.index,name='index'),
    path('xml',views.XmlView.as_view(),name='xml'),
]


