from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Todo

class TodoCreate(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ["title", "description", "completed"]
    template_name = "todo/todo_create.html"
    success_url = reverse_lazy("todo-list")

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super(TodoCreate, self).form_valid(form)

class TodoList(LoginRequiredMixin, ListView):
    model = Todo
    template_name = "todo/todo_list.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(author=self.request.user)
        context["count"] = context["tasks"].filter(completed=False).count()

        search_input = self.request.GET.get("search-area") or " "

        if search_input:
            context["tasks"] = context["tasks"].filter(title__icontains = search_input)
            context["search_input"] = search_input

        return context

class TodoDetail(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = "todo/todo_detail.html"
    context_object_name = "tasks"

class TodoUpdate(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ["title", "description", "completed"]
    context_object_name = "tasks"
    template_name = "todo/todo_update.html"
    success_url = reverse_lazy("todo-list")

class TodoDelete(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = "todo/todo_delete.html"
    context_object_name = "tasks"
    success_url = reverse_lazy("todo-list")

class CustomLoginView(LoginView):
    template_name = "todo/login.html"
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy("todo-list")

class RegisterPage(FormView):
    template_name = "todo/register.html"
    fields = "__all__"
    form_class = UserCreationForm
    success_url = reverse_lazy("todo-list")

    def form_valid(self, form):
        user = form.save()

        if user is not None:
            login(self.request, user)

        return super(RegisterPage, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("todo-list")

        return super(RegisterPage, self).get(request, *args, **kwargs)