from django.urls import path, re_path

from .views import SeriesDetail, SeriesLists, SermonDetail, SermonList, add_likes_to_sermons


urlpatterns = [
    # Sermons
    re_path('sermons/(?P<pk>\\d+)/add_lik', add_likes_to_sermons),
    path('sermons/<int:pk>/', SermonDetail.as_view(), name='sermon-detail'),
    path('', SermonList.as_view()),

    # Series API
    path('series/<int:pk>/', SeriesDetail.as_view(), name='series-detail'),
    path('series/', SeriesLists.as_view()),
]
