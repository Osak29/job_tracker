from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # Enregistre l'utilisateur en base de données
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username} ! Tu peux te connecter.')
            return redirect('login') # Redirige vers la page de login
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


