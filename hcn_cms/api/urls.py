from django.urls import include, path


urlpatterns = [
    path('sermons/', include('sermons.api.urls')),
    path('accounts/', include('accounts.api.urls'))
]
