from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class MyLoginRequiredMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы. Пожалуйста авторизуйтесь')
        url = reverse_lazy('login')
        return redirect(url)


class UserPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.get_object()
        return self.request.user.id == user.id

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для изменения другого пользователя.")
        url = reverse_lazy('users')
        return redirect(url)


class TaskPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        url = reverse_lazy('tasks')
        messages.error(self.request, "Задачу может изменить только её автор")
        return redirect(url)
