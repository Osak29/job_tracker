from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.decorators import login_required
from .models import Application
from datetime import date, timedelta

# --- FORMULAIRE ---
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        # On exclut 'user' (géré en vue) et 'date_relance' (géré par l'action rapide)
        exclude = ('user', 'date_relance')
        # On peut ajouter des widgets Bootstrap pour les dates
        widgets = {
            'date_applied': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Google'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Développeur Python'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# --- VUES ---

@login_required
def application_list(request):
    """Affiche toutes les candidatures et calcule le nombre de relances à faire."""
    apps = Application.objects.filter(user=request.user).order_by('-date_applied')
    
    # Calcul des relances : 'sent' depuis + de 7 jours et jamais relancé
    il_y_a_une_semaine = date.today() - timedelta(days=7)
    nb_relances = apps.filter(
        status='sent', 
        date_applied__lte=il_y_a_une_semaine, 
        date_relance__isnull=True
    ).count()

    return render(request, 'applications/list.html', {
        'apps': apps,
        'nb_relances': nb_relances
    })

@login_required
def application_create(request):
    """Création d'une nouvelle candidature."""
    form = ApplicationForm(request.POST or None)
    if form.is_valid():
        app = form.save(commit=False)
        app.user = request.user
        app.save()
        return redirect('application_list')
    return render(request, 'applications/form.html', {'form': form})

@login_required
def application_update(request, id):
    """Modification d'une candidature existante."""
    app = get_object_or_404(Application, id=id, user=request.user)
    form = ApplicationForm(request.POST or None, instance=app)
    if form.is_valid():
        form.save()
        return redirect('application_list')
    return render(request, 'applications/form.html', {'form': form})

@login_required
def application_delete(request, id):
    """Suppression sécurisée."""
    app = get_object_or_404(Application, id=id, user=request.user)
    if request.method == 'POST':
        app.delete()
        return redirect('application_list')
    # On peut réutiliser form.html ou un template de confirmation
    return render(request, 'applications/list.html', {'apps': Application.objects.filter(user=request.user)})

@login_required
def mark_as_relanced(request, id):
    """Action rapide : Marque comme relancé aujourd'hui."""
    app = get_object_or_404(Application, id=id, user=request.user)
    app.status = 'relance'
    app.date_relance = date.today()
    app.save()
    return redirect('application_list')

@login_required
def relance_list(request):
    """Page dédiée affichant uniquement les entreprises à relancer."""
    il_y_a_une_semaine = date.today() - timedelta(days=7)
    apps_a_relancer = Application.objects.filter(
        user=request.user, 
        status='sent', 
        date_applied__lte=il_y_a_une_semaine,
        date_relance__isnull=True
    )
    return render(request, 'applications/list.html', {
        'apps': apps_a_relancer, 
        'is_relance_view': True
    })