from django.urls import path, re_path

from .views import (
    SeriesDetail,
    SeriesLists,
    SermonDetail,
    SermonList,
    add_to_bookmark,
    update_likes_on_resource,
    list_bookmarks
)


urlpatterns = [
    # Sermons
    re_path(r'(?P<pk>\d+)/(?P<action>add_like|remove_like)/$', update_likes_on_resource, {'model': 'sermon'}),
    re_path(r'(?P<pk>\d+)/add_bookmark/$', add_to_bookmark, {'model': 'sermon'}),
    path('bookmarks/', list_bookmarks, {'model': 'sermon'}),
    path('<int:pk>/', SermonDetail.as_view(), name='sermon-detail'),
    path('', SermonList.as_view(), name='sermon-lists'),

    # Series API
    re_path(r'series/$', SeriesLists.as_view(), name='series-list'),
    re_path(r'series/bookmarks/$', list_bookmarks, {'model': 'series'}),
    re_path(r'series/(?P<pk>\d+)/(?P<action>add_like|remove_like)/$', update_likes_on_resource, {"model": "series"}),
    re_path(r'series/(?P<pk>\d+)/add_bookmark/$', add_to_bookmark, {'model': 'series'}),
    path('series/<int:pk>/', SeriesDetail.as_view(), name='series-detail'),

]
