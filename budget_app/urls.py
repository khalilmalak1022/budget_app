from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', lambda request: redirect('login')),

    # Auth
    path('', include('apps.accounts.urls')),

    # Modules principaux
    path('transactions/', include('apps.transactions.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('objectifs/', include('apps.objectifs.urls')),
    path('budgets/', include('apps.budgets.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('export/', include('apps.export.urls')),
    path('chatbot/', include('apps.chatbot.urls')),
]