from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import TodoList, TodoDetail, TodoUpdate, TodoDelete, TodoCreate, CustomLoginView, RegisterPage 

urlpatterns = [
    path("", TodoList.as_view(), name="todo-list"),
    path("todo/<int:pk>/", TodoDetail.as_view(), name="todo-detail"),
    path("task-edit/<int:pk>/", TodoUpdate.as_view(), name="todo-update"),
    path("task-delete/<int:pk>/", TodoDelete.as_view(), name="todo-delete"),
    path("task-create/",TodoCreate.as_view(), name="todo-create"),

    path("login/", CustomLoginView.as_view(), name="login"),
    path("register", RegisterPage.as_view(), name="register"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout")
    
]