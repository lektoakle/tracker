from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Ticket, Status
from django import forms

class TicketListView(ListView):
    model = Ticket

class TicketCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Ticket
    fields = ['title', 'content', 'assigned_to', 'date_due']
    # ticket_title is defined in get_success_message
    success_message = "Ticket \"%(ticket_title)s\" created successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # get_or_create returns a tuple (object, created) with object and boolean
        form.instance.status, _ = Status.objects.get_or_create(title='Not started')
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            ticket_title=self.object.title,
        )

    # widgets = {
    #     'date_due': forms.DateTimeInput()
    # }

class TicketDetailView(DetailView):
    model = Ticket 

class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Ticket
    fields = ['title', 'content', 'assigned_to', 'date_due', 'status']
    success_message = "Ticket \"%(ticket_title)s\" is updated"

    def test_func(self):
        ticket = self.get_object()
        if ticket.created_by == self.request.user:
            return True
        return False

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            ticket_title = self.object.title,
        )
        

class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy('ticket-list')
    success_message = "Ticket was deleted successfully"

    def test_func(self):
        ticket = self.get_object()
        if ticket.created_by == self.request.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(TicketDeleteView, self).delete(request, *args, **kwargs)