from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook
from apps.transactions.models import Transaction


@login_required
def export_excel(request):
    if request.method == "POST":
        date_debut = request.POST.get("date_debut")
        date_fin = request.POST.get("date_fin")

        transactions = Transaction.objects.filter(user=request.user).order_by("date")

        if date_debut:
            transactions = transactions.filter(date__gte=date_debut)

        if date_fin:
            transactions = transactions.filter(date__lte=date_fin)

        wb = Workbook()
        ws = wb.active
        ws.title = "Transactions"

        ws.append(["Date", "Description", "Catégorie", "Type", "Montant", "Solde cumulé"])

        solde = 0

        for t in transactions:
            montant = float(t.montant)

            if t.type == "revenu":
                solde += montant
            else:
                solde -= montant

            ws.append([
                t.date.strftime("%d/%m/%Y"),
                t.description,
                t.categorie.nom if t.categorie else "Sans catégorie",
                t.type,
                montant,
                solde
            ])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="transactions.xlsx"'

        wb.save(response)
        return response

    return render(request, "export/export.html")