from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:pk>/", views.listing, name="listing"),
    path("categories/", views.categories, name="categories"),
    path("category/<str:category>/", views.category, name="category"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/remove/<int:listing_pk>/",
         views.watchlist_remove, name="watchlist_remove"),
    path("watchlist/add/<int:listing_pk>",
         views.watchlist_add, name="watchlist_add"),
    path("close/<int:pk>/", views.close, name="close"),
    path("comment/<int:pk>/", views.comment, name="comment"),

]
