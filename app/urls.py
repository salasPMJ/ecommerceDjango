from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    # PARA NO AÑADIR /APP/ A LA RUTA
    path('', views.home_redirect),

    # path('home/', views.home),

    # PAGINA INDEX
    path('index/', views.index_load, name="index_load"),


    # LOGIN
    path('accounts/login', views.do_login, name="login"),
    path('accounts/logout', views.do_logout, name="logout"),
    path('accounts/register', views.do_register, name="register"),


    # PROFILE
    path('profiles/profile', views.profile_create, name="profile"),


    # CRUD PRODUCTS
    path('products/', views.product_list, name="product_list"),
    path('products/new', views.product_new, name="product_new"),
    path('products/<int:id>/load', views.product_load, name="product_load"),
    path('products/filter/', views.product_filter, name="product_filter"),
    path('products/save', views.product_save, name="product_save"),
    path('products/<int:id>/view', views.product_view, name="product_view"),
    path('products/<int:pk>/delete', views.product_delete, name="product_delete"),


    # CRUD CART
    path('carts/<int:product_id>/add', views.cart_add_product, name="cart_add_product"),
    path('carts/<int:product_id>/delete', views.cart_delete_product, name="cart_delete_product"),
    path('carts/<int:product_id>/reduce', views.cart_reduce_product, name="cart_reduce_product"),
    path('carts/<int:product_id>/clean', views.cart_clean, name="cart_clean"),



]