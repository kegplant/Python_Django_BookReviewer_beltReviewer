from django.conf.urls import url
from . import views #this line is new! #imports views.py from current folder
urlpatterns=[
    url(r'^$', views.index),#this line has changed!,
    url(r'^process$', views.process),
    url(r'^clear$', views.clear),
    url(r'^(?P<id>\d+)/success$', views.success),
    url(r'^logOut$', views.logOut),

    url(r'^books$', views.books),
    url(r'^books/add$', views.books_add),
    url(r'^books/create$', views.books_create),
    url(r'^review/create$', views.review_create),
    url(r'^books/(?P<book_id>\d+)$', views.books_show),
    url(r'^review/(?P<review_id>\d+)/destroy$', views.review_destroy),
    url(r'^users/(?P<id>\d+)$', views.users),
]
  