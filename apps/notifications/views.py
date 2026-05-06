from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def notifications(request):
    return render(request, 'notifications/liste.html')