from django.contrib import admin

from .models import Category, Comment, Company, Complaint, ComplaintBacker, Region, StatusHistory

admin.site.register(Category)
admin.site.register(Company)
admin.site.register(Region)
admin.site.register(Complaint)
admin.site.register(ComplaintBacker)
admin.site.register(Comment)
admin.site.register(StatusHistory)
