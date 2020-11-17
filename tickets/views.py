from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Ticket, Status

class TicketListView(ListView):
    model = Ticket

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['title', 'content', 'assigned_to', 'date_due']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.status = Status.objects.get(title='Not started')
        return super().form_valid(form)

class TicketDetailView(DetailView):
    model = Ticket 

class TicketUpdateView(UpdateView):
    model = Ticket
    fields = ['title', 'content', 'assigned_to', 'date_due', 'status']

class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('ticket-list')