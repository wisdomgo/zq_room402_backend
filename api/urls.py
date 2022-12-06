from django.urls import path, include, re_path

from api import views

urlpatterns = [
    path("users", views.UserInfoView.as_view()),
    path("users/<int:pk>", views.UserInfoDetailView.as_view()),
    path("users/<int:pk>/details", views.UserDetailInfoView.as_view()),
    path("users/records", views.RecordInfoView.as_view()),
    path("users/<int:pk>/records", views.UserRecordInfoView.as_view()),
    path("users/<int:pk1>/records/<int:pk2>", views.UserRecordInfoDetailView.as_view()),
    path("whereiskey", views.KeyInfoView.as_view()),
]
