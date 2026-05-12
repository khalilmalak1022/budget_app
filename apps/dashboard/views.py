from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from dateutil.relativedelta import relativedelta

from apps.transactions.models import Transaction, Categorie
from apps.budgets.models import Budget
from apps.notifications.models import Notification


MOIS_FR = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
]


@login_required
def dashboard(request):
    today = date.today()

    # ─── Filtre mois ─────────────────────────────────────────────────────────────
    mois_param = request.GET.get('mois', '')
    try:
        annee_filtre, mois_filtre = int(mois_param.split('-')[0]), int(mois_param.split('-')[1])
    except Exception:
        annee_filtre, mois_filtre = today.year, today.month

    transactions_mois = Transaction.objects.filter(
        user=request.user,
        date__month=mois_filtre,
        date__year=annee_filtre,
    )

    total_revenus  = transactions_mois.filter(type='revenu').aggregate(total=Sum('montant'))['total'] or 0
    total_depenses = transactions_mois.filter(type='depense').aggregate(total=Sum('montant'))['total'] or 0
    solde          = float(total_revenus) - float(total_depenses)

    # ─── Camembert dépenses par catégorie ────────────────────────────────────────
    depenses_par_cat = (
        transactions_mois.filter(type='depense')
        .values('categorie__nom', 'categorie__couleur')
        .annotate(total=Sum('montant'))
        .order_by('-total')
    )
    labels_camembert   = [d['categorie__nom'] or 'Sans catégorie' for d in depenses_par_cat]
    valeurs_camembert  = [float(d['total']) for d in depenses_par_cat]
    couleurs_camembert = [d['categorie__couleur'] or '#6c63ff' for d in depenses_par_cat]

    # ─── Graphique barres 6 mois ──────────────────────────────────────────────────
    labels_barres   = []
    revenus_barres  = []
    depenses_barres = []
    for i in range(5, -1, -1):
        d = date(annee_filtre, mois_filtre, 1) - relativedelta(months=i)
        labels_barres.append(f"{MOIS_FR[d.month - 1][:3]} {d.year}")
        r = Transaction.objects.filter(
            user=request.user, type='revenu',
            date__month=d.month, date__year=d.year
        ).aggregate(total=Sum('montant'))['total'] or 0
        dep = Transaction.objects.filter(
            user=request.user, type='depense',
            date__month=d.month, date__year=d.year
        ).aggregate(total=Sum('montant'))['total'] or 0
        revenus_barres.append(float(r))
        depenses_barres.append(float(dep))

    # ─── Courbe ligne 12 mois ─────────────────────────────────────────────────────
    labels_ligne   = []
    depenses_ligne = []
    for i in range(11, -1, -1):
        d = date(annee_filtre, mois_filtre, 1) - relativedelta(months=i)
        labels_ligne.append(f"{MOIS_FR[d.month - 1][:3]} {d.year}")
        dep = Transaction.objects.filter(
            user=request.user, type='depense',
            date__month=d.month, date__year=d.year
        ).aggregate(total=Sum('montant'))['total'] or 0
        depenses_ligne.append(float(dep))

    # ─── Alertes budgets dépassés ─────────────────────────────────────────────────
    budgets_mois = Budget.objects.filter(
        user=request.user,
        periode__month=mois_filtre,
        periode__year=annee_filtre,
    ).select_related('categorie')

    alertes = []
    for budget in budgets_mois:
        depense_cat = transactions_mois.filter(
            type='depense', categorie=budget.categorie
        ).aggregate(total=Sum('montant'))['total'] or 0
        if depense_cat > budget.montant_limite:
            alertes.append({
                'categorie':   budget.categorie.nom,
                'limite':      float(budget.montant_limite),
                'depense':     float(depense_cat),
                'depassement': float(depense_cat - budget.montant_limite),
            })

    # ─── Conseil intelligent ──────────────────────────────────────────────────────
    conseil      = None
    conseil_type = 'success'
    if total_depenses == 0 and total_revenus == 0:
        conseil      = "📊 Commencez à enregistrer vos transactions pour obtenir des conseils personnalisés."
        conseil_type = 'info'
    elif alertes:
        cat_depasse  = alertes[0]['categorie']
        conseil      = f"⚠️ Vos dépenses en <strong>{cat_depasse}</strong> ont dépassé le budget ce mois-ci."
        conseil_type = 'danger'
    elif total_depenses > total_revenus:
        conseil      = "🚨 Vos dépenses dépassent vos revenus ce mois. Attention à votre solde !"
        conseil_type = 'danger'
    elif total_depenses > 0 and total_revenus > 0:
        ratio = (float(total_depenses) / float(total_revenus)) * 100
        if ratio > 80:
            conseil      = f"⚠️ Vous avez dépensé <strong>{ratio:.0f}%</strong> de vos revenus. Essayez d'épargner davantage."
            conseil_type = 'warning'
        elif ratio > 50:
            conseil      = f"💡 Vous dépensez {ratio:.0f}% de vos revenus. Vous pouvez encore optimiser."
            conseil_type = 'warning'
        else:
            conseil      = f"✅ Excellent ! Vous n'avez dépensé que <strong>{ratio:.0f}%</strong> de vos revenus !"
            conseil_type = 'success'
    elif total_revenus > 0:
        conseil      = "✅ Bon travail ! Aucune dépense enregistrée ce mois-ci."
        conseil_type = 'success'

    # ─── Comparaison mois précédent ───────────────────────────────────────────────
    mois_prec  = mois_filtre - 1 if mois_filtre > 1 else 12
    annee_prec = annee_filtre if mois_filtre > 1 else annee_filtre - 1

    depenses_mois_prec = Transaction.objects.filter(
        user=request.user, type='depense',
        date__month=mois_prec, date__year=annee_prec
    ).aggregate(total=Sum('montant'))['total'] or 0

    revenus_mois_prec = Transaction.objects.filter(
        user=request.user, type='revenu',
        date__month=mois_prec, date__year=annee_prec
    ).aggregate(total=Sum('montant'))['total'] or 0

    variation_depenses = 0
    variation_revenus  = 0
    if depenses_mois_prec > 0:
        variation_depenses = ((float(total_depenses) - float(depenses_mois_prec)) / float(depenses_mois_prec)) * 100
    if revenus_mois_prec > 0:
        variation_revenus  = ((float(total_revenus)  - float(revenus_mois_prec))  / float(revenus_mois_prec))  * 100

    # ─── Score santé financière ───────────────────────────────────────────────────
    score_sante = 100
    if total_revenus > 0:
        ratio_dep = float(total_depenses) / float(total_revenus)
        score_sante = max(0, int(100 - (ratio_dep - 1) * 100)) if ratio_dep > 1 else int(100 - ratio_dep * 40)
    if alertes:
        score_sante = max(0, score_sante - len(alertes) * 10)

    if score_sante >= 80:   score_label, score_couleur = "Excellent",    "success"
    elif score_sante >= 60: score_label, score_couleur = "Bon",          "info"
    elif score_sante >= 40: score_label, score_couleur = "À améliorer",  "warning"
    else:                   score_label, score_couleur = "Critique",     "danger"

    # ─── Notifications non lues ───────────────────────────────────────────────────
    notifications_non_lues = Notification.objects.filter(
        user=request.user, est_lue=False
    ).count()

    # ─── Dernières transactions ───────────────────────────────────────────────────
    dernieres_transactions = Transaction.objects.filter(
        user=request.user
    ).select_related('categorie').order_by('-date')[:5]

    # ─── Liste mois disponibles ───────────────────────────────────────────────────
    mois_disponibles = []
    for i in range(11, -1, -1):
        m = mois_filtre - i
        a = annee_filtre
        while m <= 0:
            m += 12
            a -= 1
        mois_disponibles.append({
            'valeur':      f"{a}-{m:02d}",
            'label':       f"{MOIS_FR[m - 1]} {a}",
            'selectionne': (m == mois_filtre and a == annee_filtre),
        })

    context = {
        'total_revenus':          total_revenus,
        'total_depenses':         total_depenses,
        'solde':                  solde,
        'labels_camembert':       labels_camembert,
        'valeurs_camembert':      valeurs_camembert,
        'couleurs_camembert':     couleurs_camembert,
        'labels_barres':          labels_barres,
        'revenus_barres':         revenus_barres,
        'depenses_barres':        depenses_barres,
        'labels_ligne':           labels_ligne,
        'depenses_ligne':         depenses_ligne,
        'alertes':                alertes,
        'notifications_non_lues': notifications_non_lues,
        'conseil':                conseil,
        'conseil_type':           conseil_type,
        'variation_depenses':     round(variation_depenses, 1),
        'variation_revenus':      round(variation_revenus,  1),
        'depenses_mois_prec':     depenses_mois_prec,
        'revenus_mois_prec':      revenus_mois_prec,
        'score_sante':            score_sante,
        'score_label':            score_label,
        'score_couleur':          score_couleur,
        'dernieres_transactions': dernieres_transactions,
        'mois_actuel':            today.strftime('%B %Y'),
        'mois_filtre':            f"{annee_filtre}-{mois_filtre:02d}",
        'mois_disponibles':       mois_disponibles,
    }

    return render(request, 'dashboard/dashboard.html', context)