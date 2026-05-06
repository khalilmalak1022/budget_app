from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def export_excel(request):
    return render(request, 'export/export.html')