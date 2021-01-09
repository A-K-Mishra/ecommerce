#this file is similar to one in our CoreyShafer folder 
from django.urls import path # path function maps an url to a particular view that we create in views.py , basically creates an alias for written URL to passed path 
# we also need to include home fucntion in views.py , so we need to import views.py as well
from . import views
from .views import ProductCreateView,OrderCreateView,OrderDetailView , OrderDeleteView , OrderListView , ProductUpdateView , ProductListView
#from .views import PostListView#, PostDetailView ,PostCreateView,PostUpdateView , PostDeleteView , UserPostView

# urlpatterns is basically a list containing a mapping of path to directories or functions 
urlpatterns =[
    
    path('',views.home,name="products-home") , # here basically we say that when user lands on home page , i.e , the URL is empty , we map it to home function in views.py to handle , we have provided a name to that path 'blog-home'
                                           # when we match blog/ at urls.py in our main(project) folder , the remaining string is only sent here , thus an user searching for blog/ will make the urls.py in the project folder send an empty string(as it is only the part that is not matched or everything matches)
    path('forbidden/',views.forbidden,name="forbidden") ,
    path('order-update/<int:pk>/', views.addItem, name = "order-update" ) ,
    path('order-remove/<int:pk>/<int:pk1>', views.removeItem, name = "order-remove" ) ,
    path('order-place/<int:pk>/', views.place_order, name = "place-order" ) ,
    path('add_to_cart/<int:pk>/<int:pk1>/', views.add_to_cart, name = "add-to-cart" ) ,
    path('remove_from_cart/<int:pk>/<int:pk1>/', views.remove_from_cart, name = "remove-from-cart" ) ,
    path('cart/', views.view_cart, name = "cart-detail" ) ,
    #path('',PostListView.as_view(),name="products-home") ,#added in video 10
                                                      # this type of view looks for <app>/<model>_<viewtype>.html by default but we can change it to our pre existing home template in views.py
    #path('user/<str:username>',UserPostView.as_view(),name="user-posts"),
    #path('post/<int:pk>/',PostDetailView.as_view(),name="post-detail") ,
    #path('post/<int:pk>/update/',PostUpdateView.as_view(),name="post-update") ,
    #path('post/<int:pk>/delete/',PostDeleteView.as_view(),name="post-delete") ,
    path('new/',ProductCreateView.as_view(),name="product-create") ,# this type of view expects <app>/<model>_form.html
    path('product-update/<int:pk>',ProductUpdateView.as_view(),name="product-update") ,
    path('order/<int:pk>/', OrderCreateView.as_view() ,name ="order-create"),
    path('order-detail/<int:pk>/', OrderDetailView.as_view() ,name ="order-detail"),
    path('order-item-delete/<int:pk>/', views.delete_order,name ="order-item-delete"),
    path('order-delete/<int:pk>/', OrderDeleteView.as_view() ,name ="order-delete"),
    path('user-order/<str:username>/',OrderListView.as_view() , name = "user-order"),
    path('user-products/<str:username>/',ProductListView.as_view() , name = "user-products"),
    #path('order-detail/<int:pk>/', DeleteFromOrderView.as_view() ,name ="order-detail"),

    #path('about/',views.about , name='products-about') , #an user searching for blog/about/ will have urls.py send only 'about/' string here as blog/ ia already matched , so that is how we decide heirarchy 
]