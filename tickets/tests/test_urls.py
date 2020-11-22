from django.test import SimpleTestCase
from django.urls import reverse, resolve
from tickets.views import (
    TicketCreateView,
    TicketDeleteView,
    TicketDetailView,
    TicketListView,
    TicketUpdateView
)


class TestUrls(SimpleTestCase):

    def test_ticket_list_resolves(self):
        url = reverse('ticket-list')
        self.assertEqual(resolve(url).func.view_class, TicketListView)

    def test_ticket_detail_resolves(self):
        url = reverse('ticket-detail',args='2')
        self.assertEqual(resolve(url).func.view_class, TicketDetailView)

    def test_ticket_create_resolves(self):
        url = reverse('ticket-create')
        self.assertEqual(resolve(url).func.view_class, TicketCreateView)

    def test_ticket_update_resolves(self):
        url = reverse('ticket-update',args='2')
        self.assertEqual(resolve(url).func.view_class, TicketUpdateView)

    def test_ticket_delete_resolves(self):
        url = reverse('ticket-delete',args='1')
        self.assertEqual(resolve(url).func.view_class, TicketDeleteView)