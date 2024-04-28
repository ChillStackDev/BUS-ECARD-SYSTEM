from django.urls import path
from .views import recharge,success,api,fail,email_template
urlpatterns = [
   path('',recharge,name='recharge'),
   path('success',success,name='success'),
   path('fail',fail,name='fail'),
   path('api',api,name='api'),
   path('email',email_template,name='email_template')
]