from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transaction, Categorie
from .forms import TransactionForm, CategorieForm

@login_required
def transaction_liste(request):
    transactions = Transaction.objects.filter(
        user=request.user).order_by('-date')
    return render(request, 'transactions/liste.html',
        {'transactions': transactions})

@login_required
def transaction_ajouter(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction ajoutée !')
            return redirect('transaction_liste')
    else:
        form = TransactionForm()
    form.fields['categorie'].queryset = Categorie.objects.filter(
        user=request.user)
    return render(request, 'transactions/form.html', {'form': form})

@login_required
def transaction_modifier(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction modifiée !')
            return redirect('transaction_liste')
    else:
        form = TransactionForm(instance=transaction)
    form.fields['categorie'].queryset = Categorie.objects.filter(
        user=request.user)
    return render(request, 'transactions/form.html', {'form': form})

@login_required
def transaction_supprimer(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction supprimée !')
        return redirect('transaction_liste')
    return render(request, 'transactions/confirm_delete.html',
        {'obj': transaction})

@login_required
def categorie_liste(request):
    categories = Categorie.objects.filter(user=request.user)
    return render(request, 'transactions/categories/liste.html',
        {'categories': categories})

@login_required
def categorie_ajouter(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            categorie = form.save(commit=False)
            categorie.user = request.user
            categorie.save()
            messages.success(request, 'Catégorie ajoutée !')
            return redirect('categorie_liste')
    else:
        form = CategorieForm()
    return render(request, 'transactions/categories/form.html', {'form': form})

@login_required
def categorie_modifier(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie modifiée !')
            return redirect('categorie_liste')
    else:
        form = CategorieForm(instance=categorie)
    return render(request, 'transactions/categories/form.html', {'form': form})

@login_required
def categorie_supprimer(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk, user=request.user)
    if request.method == 'POST':
        categorie.delete()
        messages.success(request, 'Catégorie supprimée !')
        return redirect('categorie_liste')
    return render(request, 'transactions/categories/confirm_delete.html',
        {'obj': categorie})

@login_required
def historique(request):
    transactions = Transaction.objects.filter(
        user=request.user).order_by('-date')
    q = request.GET.get('q')
    categorie = request.GET.get('categorie')
    type_ = request.GET.get('type')
    if q:
        transactions = transactions.filter(description__icontains=q)
    if categorie:
        transactions = transactions.filter(categorie__id=categorie)
    if type_:
        transactions = transactions.filter(type=type_)
    categories = Categorie.objects.filter(user=request.user)
    return render(request, 'transactions/historique.html', {
        'transactions': transactions,
        'categories': categories,
    })