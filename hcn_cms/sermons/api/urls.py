from django.urls import path, re_path

from .views import SeriesDetail, SeriesLists, SermonDetail, SermonList, add_likes_to_sermons, remove_like_from_sermon


urlpatterns = [
    # Sermons
    re_path('(?P<pk>\\d+)/add_like', add_likes_to_sermons),
    re_path('(?P<pk>\\d+)/remove_like', remove_like_from_sermon),
    path('<int:pk>/', SermonDetail.as_view(), name='sermon-detail'),
    path('', SermonList.as_view(), name='sermon-lists'),

    # Series API
    path('series/<int:pk>/', SeriesDetail.as_view(), name='series-detail'),
    path('series/', SeriesLists.as_view(), name='series-list'),
]
