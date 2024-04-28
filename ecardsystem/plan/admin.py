from django.contrib import admin
from .models import Plan, UserSubscription,UserTimeline

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'duration_months', 'coins')

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('uid', 'plan', 'start_date', 'end_date', 'coins','paid')

admin.site.register(UserTimeline)