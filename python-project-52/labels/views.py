from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from labels.forms import LabelForm
from labels.models import Label
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _


def index(request):
    labels = Label.objects.all()
    return render(request, 'labels/index.html', {'labels': labels})


class CreateLabelView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully created')


class UpdateLabelView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully updated')


class DeleteLabelView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully deleted')

    def post(self, request, *args, **kwargs):
        if self.get_object().task_set.count():
            messages.warning(self.request, _('It`s not possible to delete the label that is being used'))
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
