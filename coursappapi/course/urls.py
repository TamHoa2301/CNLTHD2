from django.urls import path, re_path, include
from rest_framework import routers
from course import views

r = routers.DefaultRouter()
r.register('categories', views.CategoryViewset, basename='categories')
r.register('courses', views.CourseViewset, basename='courses')
r.register('lessons', views.LessonViewset, basename='lessons')
r.register('users', views.UserViewSet, basename='users')
r.register('comment', views.CommentViewSet, basename='comments')




urlpatterns = [
    path('', include(r.urls))
]