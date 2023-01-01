from django.urls import path, include
from . import views

app_name = 'App_Blog'

# Tham khảo StackOverFlow: https://stackoverflow.com/questions/31491028/django-generic-views-based-as-view-method
urlpatterns = [
    path('',views.BlogList.as_view(),name='list_all_blog'),
    # Trong Class Based View, phải gọi function as_view() để có thể trả về một view lấy request và trả về response 
    # as_view là một function(class method) mà kế nối BlogCreation class với URLs của chính nó
    path('write/',views.BlogCreation.as_view(),name='create_blog'),
    path('details/<slug:slug>',views.blog_details,name='blog_details'),
    path('my-blog/',views.MyBlogs.as_view(),name='my_blogs'),
    path('edit-blog/<pk>/',views.UpdateBlog.as_view(),name='edit_blog'),
]
