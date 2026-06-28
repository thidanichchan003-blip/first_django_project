from django.contrib import admin
from .models import Consultation, Message, Notification

admin.site.register(Message)
admin.site.register(Notification)

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1
    fields = ['sender', 'message', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    inlines = [MessageInline]