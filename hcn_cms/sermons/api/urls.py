from django.urls import path, re_path

from .views import (
    SeriesDetail,
    SeriesLists,
    SermonDetail,
    SermonList,
    add_to_bookmark,
    already_bookmarked,
    my_bookmarks,
    update_likes_on_resource,
)


urlpatterns = [
    # Series API
    re_path(r'series/$', SeriesLists.as_view(), name='series-list'),
    re_path(r'series/bookmarks/$', my_bookmarks, {'model': 'series'}),
    re_path(r'series/(?P<pk>\d+)/(?P<action>add_like|remove_like)/$', update_likes_on_resource, {"model": "series"}),
    re_path(r'series/(?P<pk>\d+)/add_bookmark/$', add_to_bookmark, {'model': 'series'}),
    re_path(r'series/(?P<pk>\d+)/liked_by_user/$', already_bookmarked, {'model': 'series'}),
    path('series/<int:pk>/', SeriesDetail.as_view(), name='series-detail'),

    # Sermons
    re_path(r'(?P<pk>\d+)/(?P<action>add_like|remove_like)/$', update_likes_on_resource, {'model': 'sermon'}),
    path('bookmarks/', my_bookmarks, {'model': 'sermon'}),
    path('<int:pk>/', SermonDetail.as_view(), name='sermon-detail'),
    re_path('(?P<pk>\\d+)/liked_by_user', already_bookmarked, {'model': 'sermon'}),
    path('', SermonList.as_view(), name='sermon-lists'),
    re_path(r'(?P<pk>\d+)/add_bookmark/$', add_to_bookmark, {'model': 'sermon'}),
]
