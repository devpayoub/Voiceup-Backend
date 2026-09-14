from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5MB


def validate_photo_size(value):
    if value.size > MAX_PHOTO_SIZE:
        raise ValidationError('Photo must be smaller than 5MB.')


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Complaint(models.Model):
    STATUS_RECEIVED = 'received'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_RESOLVED = 'resolved'
    STATUS_CHOICES = [
        (STATUS_RECEIVED, 'Received'),
        (STATUS_IN_PROGRESS, 'In progress'),
        (STATUS_RESOLVED, 'Resolved'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='complaints')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='complaints')
    title = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='complaints/', blank=True, null=True, validators=[validate_photo_size])
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_RECEIVED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ComplaintBacker(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='backers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='backed_complaints')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('complaint', 'user')


class Comment(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class StatusHistory(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20, choices=Complaint.STATUS_CHOICES)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
