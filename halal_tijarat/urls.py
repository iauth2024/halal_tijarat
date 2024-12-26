# halal_tijarat/urls.py
from django.contrib import admin
from django.urls import path, include  # include is used to include app urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('muqaddar.urls')),  # This includes the app's URLs
    
]
