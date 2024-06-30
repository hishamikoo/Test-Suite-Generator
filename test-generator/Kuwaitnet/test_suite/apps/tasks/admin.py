from django.contrib import admin
from .models import Task, Attachment, Suite

admin.site.register(Task)
admin.site.register(Attachment)
admin.site.register(Suite)