from django.urls import include, path


urlpatterns = [
    path('sermons/', include('sermons.api.urls'))
]
