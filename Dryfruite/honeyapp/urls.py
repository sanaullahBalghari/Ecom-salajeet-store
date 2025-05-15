from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register_view, name="register_view"),
    path('login/', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout_view"),
    path('about/', views.about, name="about"),
    path('products/', views.productlist, name="products"),
    path('detail/<int:id>/', views.detail, name="detail"),
    path('carts/', views.carts, name="carts"),
    path('add_product/', views.add_product, name="add_product"),
    path('delete_product/<int:id>/', views.delete_product, name="delete_product"),
    path('update_product/<int:id>/', views.update_product, name="update_product"),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('delete_cart_item/<int:id>/', views.delete_cart_item, name='delete_cart_item'),
    path('contact/', views.contact, name='contact'),
  
    
]