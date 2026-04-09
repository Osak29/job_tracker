from django.urls import path
from . import views

urlpatterns = [
    path('', views.application_list, name='application_list'),
    path('add/', views.application_create, name='application_create'),
    path('update/<int:id>/', views.application_update, name='application_update'),
    path('delete/<int:id>/', views.application_delete, name='application_delete'),
    path('relancer/<int:id>/', views.mark_as_relanced, name='mark_as_relanced'),
]