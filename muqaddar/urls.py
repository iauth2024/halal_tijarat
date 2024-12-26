from django.urls import path
from . import views


urlpatterns = [
    path('combined_results/', views.combined_results, name='combined_results'),
    path('', views.screener_results, name='screener_results'),
    path('performance/', views.performance_page, name='performance_page'),
    path('delete-selected-stocks/', views.delete_selected_stocks, name='delete_selected_stocks'),


]
