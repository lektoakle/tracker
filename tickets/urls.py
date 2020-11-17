from django.urls import path
from .views import (
    TicketListView, 
    TicketCreateView, 
    TicketDetailView, 
    TicketUpdateView, 
    TicketDeleteView,
    )

urlpatterns = [
    path('', TicketListView.as_view(), name="ticket-list"),
    path('new/', TicketCreateView.as_view(), name="ticket-create"),
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
    path('<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
]
