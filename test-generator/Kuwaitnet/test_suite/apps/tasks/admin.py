from django.contrib import admin
from .models import Task, Attachment, Suite


class AdminArea(admin.AdminSite):
    site_header = 'Admin Area'
    login_template = 'login.html'

app_site = AdminArea(name='AppAdmin')

app_site.register(Task)
app_site.register(Attachment)
app_site.register(Suite)