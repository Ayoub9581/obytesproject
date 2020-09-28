from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import  HttpResponseForbidden
from .forms import  StatusForm
from .models import  Status




class CreateStatusView(LoginRequiredMixin,CreateView):
    model = Status
    form_class = StatusForm
    template_name= 'status/add_message.html'
    success_url = '/status/add'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateStatusView, self).form_valid(form)

    def get_permission_denied_message(self):
        return super().get_permission_denied_message()


class ListMessageView(LoginRequiredMixin,ListView):
    model = Status
    template_name = 'status/all_messages.html'
    
    def get_queryset(self):
        user = self.request.user
        qs = self.model.objects.get_messages(20, user) 
        return qs


class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/add_message.html'
    success_url = '/status/add'

