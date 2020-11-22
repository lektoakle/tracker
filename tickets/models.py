from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import get_sentinel_user

class Status(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self):
        return self.title

    class Meta():
        verbose_name_plural = 'status'


class Ticket(models.Model):
    title = models.CharField(max_length=280)
    created_by = models.ForeignKey(
        get_user_model(), 
        on_delete=models.SET(get_sentinel_user),
        related_name='ticket_created_by',
        )
    assigned_to = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name='ticket_assigned_to',
        )
    date_open = models.DateTimeField(auto_now_add=True)
    date_due = models.DateTimeField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    status = models.ForeignKey(
        Status, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True, 
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ticket-detail',kwargs={'pk': self.pk})
