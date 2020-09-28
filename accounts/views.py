from django.shortcuts import render, redirect
from django.views.generic import  FormView
from .forms import LoginForm

from obytesproject.mixins import  RequestFormAttachMixin,NextUrlMixin
class LoginView(NextUrlMixin,RequestFormAttachMixin,FormView):
    form_class = LoginForm
    template_name = "auth/login.html"
    success_url = '/'
    default_next = '/'
    
    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)
		
		
    
    