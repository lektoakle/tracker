from django.test import (
    TestCase, 
    RequestFactory,
    )
from django.urls import reverse
from tickets.models import Ticket, Status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.forms.models import model_to_dict
import datetime

class TicketListViewTest(TestCase):
    
    def test_ticket_list_view(self):
        response = self.client.get(reverse('ticket-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='ticket_list.html')

class TicketCreateViewTest(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@user.com", password="1234test")
        self.path = reverse('ticket-create')

    def test_create_view_get_anonymous_user_redirected(self):
        """User is redirected to login"""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 302)


    def test_create_view_post_anonymous_user_redirected(self):
        """Anonymous user cannot create a ticket"""
        data = {
            'title': "Test title",
            'content': "Test content"
            }
        response = self.client.post(self.path, data=data)
        self.assertEqual(response.status_code, 302)


    def test_create_view_logged_in_user(self):
        """logged in user creates ticket successfully"""
        data = {
            'title': "Test title",
            'content': "Test content"
            }
        self.client.force_login(self.user)
        response = self.client.post(self.path, data=data)
        self.assertTemplateUsed(template_name='ticket_form.html')
        new_ticket = Ticket.objects.get(title=data['title'], content=data['content'])
        self.assertEqual(new_ticket.title, data['title'])
        self.assertEqual(new_ticket.content, data['content'])
        self.assertEqual(new_ticket.created_by, self.user)
        self.assertEqual(new_ticket.status.title, "Not started")
        self.assertEqual(response.url, new_ticket.get_absolute_url())


class TicketUpdateViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@user.com", password="1234test")
        self.user0 = get_user_model().objects.create_user(email="test0@user.com", password="test1234")
        self.ticket = Ticket.objects.create(
            title="My title", 
            content="My content", 
            created_by=self.user,
        )
        self.path = reverse('ticket-update', kwargs={'pk':self.ticket.pk})
        Status.objects.create(title="Not started")

    def test_ticket_update_others_denied(self):
        """User cannot change other person's ticket"""
        self.client.force_login(self.user0)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

    def test_ticket_update_own_granted(self):
        """User can change his own ticket"""
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

     
    def test_ticket_update_view(self):
        """User can change his own ticket"""
        
        self.client.force_login(self.user)

        data = {
            'title': 'Updated title',
            'content': 'Updated content',
            'assigned_to': '1',
            'date_due': datetime.datetime.now() + datetime.timedelta(weeks=2),
            'status': '1',
            }
        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='ticket_form.html')
        
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.title, data['title'])
        self.assertEqual(self.ticket.content, data['content'])


class TicketDeleteViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@user.com", password="1234test")
        self.user0 = get_user_model().objects.create_user(email="test0@user.com", password="test1234")
        self.ticket = Ticket.objects.create(
            title="My title", 
            content="My content", 
            created_by=self.user,
        )
        self.path = reverse('ticket-delete', kwargs={'pk':self.ticket.pk})

    def test_ticket_delete_denied(self):
        """User cannot delete other person's ticket"""
        self.client.force_login(self.user0)
        request = self.client.get(self.path)
        self.assertEqual(request.status_code, 403)

    def test_ticket_delete_granted(self):
        """User can delete his own ticket"""
        self.client.force_login(self.user)
        request = self.client.get(self.path)
        self.assertEqual(request.status_code, 200)
     
    def test_ticket_delete_view(self):
        """User can delete his own ticket"""
        
        self.client.force_login(self.user)
        response = self.client.post(self.path)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='ticket_confirm_delete.html')
        with self.assertRaisesMessage(Ticket.DoesNotExist, 'Ticket matching query does not exist.'):
            Ticket.objects.get(title="My title")