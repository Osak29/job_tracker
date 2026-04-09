from django.contrib import admin
from django.urls import path, include  # <-- On ajoute 'include' ici
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentification
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', accounts_views.register, name='register'),
    
    # Inclusion des URLs de ton application de gestion de jobs
    path('applications/', include('applications.urls')),

    # Accueil : Redirige vers la liste des applications si connecté, 
    # ou vers login sinon (via la vue qu'on a configurée)
    path('', RedirectView.as_view(url='applications/', permanent=False), name='index'),
]