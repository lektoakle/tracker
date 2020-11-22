from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Ticket, Status

class TicketListView(ListView):
    model = Ticket

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['title', 'content', 'assigned_to', 'date_due']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # get_or_create return a tuple (object, created) with object and boolean
        form.instance.status, _ = Status.objects.get_or_create(title='Not started')
        return super().form_valid(form)

class TicketDetailView(DetailView):
    model = Ticket 

class TicketUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ticket
    fields = ['title', 'content', 'assigned_to', 'date_due', 'status']

    def test_func(self):
        ticket = self.get_object()
        if ticket.created_by == self.request.user:
            return True
        return False

class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy('ticket-list')

    def test_func(self):
        ticket = self.get_object()
        if ticket.created_by == self.request.user:
            return True
        return False