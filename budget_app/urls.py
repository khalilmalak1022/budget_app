from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('', include('apps.transactions.urls')),
    path('', include('apps.dashboard.urls')),
    path('', include('apps.objectifs.urls')),
    path('', include('apps.budgets.urls')),
    path('', include('apps.notifications.urls')),
    path('', include('apps.export.urls')),
    path('', include('apps.chatbot.urls')),
]