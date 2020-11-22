from django.test import TestCase, Client
from tickets.models import Ticket, Status
from django.contrib.auth import get_user_model




class TicketTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@email.com',password="1234")

    def create_ticket(self, title='Test ticket title'):
        return Ticket.objects.create(title=title, created_by=self.user)

    def test_create_ticket(self):
        t = self.create_ticket()
        self.assertIsInstance(t, Ticket)
        self.assertEqual(str(t), t.title)
        self.assertEqual(t.created_by, self.user)
        
    def test_get_absolute_url(self):
        t = self.create_ticket()
        self.assertEqual(f'/ticket/{t.id}/', t.get_absolute_url())


class StatusTest(TestCase):
    def create_status(self, title="Test"):
        return Status.objects.create(title=title)

    def test_create_status(self):
        title = "test status title"
        s = self.create_status(title=title)
        self.assertEqual(str(s), s.title)