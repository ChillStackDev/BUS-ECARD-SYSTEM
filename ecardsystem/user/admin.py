from django.contrib import admin
from .models import Student
from django.conf import settings
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'verified']

    def save_model(self, request, obj, form, change):
        if obj.verified and obj.pk and change:
            context = {
            'uid': obj.uid,
        }
            msg_html=render_to_string('approved.html',context)
            send_mail(
                subject='BUS ECARD APPROVED',
                message=f"Your unique id is {obj.uid} and reset your password by going to http://127.0.0.1:8000/reset" ,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[obj.user.email],
                html_message=msg_html
            )

        obj.save()  

admin.site.register(Student, StudentAdmin)


