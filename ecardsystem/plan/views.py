from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  
from .models import Plan, UserSubscription,UserTimeline
from user.models import Student
from datetime import date, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from datetime import datetime
import razorpay
from django.conf import settings
import json
from django.http import Http404

@login_required(login_url='/login')   
def recharge(request):
    plans = Plan.objects.all()
    subscription = None
    Timeline=None
    
    if request.method == 'POST':
        print("callllllllll")
        plan_id = request.POST.get('plan')
        selected_plan = Plan.objects.get(pk=plan_id)
        end_date = date.today() + timedelta(days=(30 * selected_plan.duration_months))
        coins = selected_plan.coins
        client=razorpay.Client(auth=(settings.KEY,settings.KEY_SECRET))
        amount_in_paisa = int(selected_plan.amount * 100)  
        payment = client.order.create({
            'amount': amount_in_paisa,
            'currency': 'INR',
            'payment_capture': 1
        })
        payment_json = json.dumps(payment)
        print(payment_json)
       
        if not request.user.student.verify_data_integrity():
            print("Data Integrity Failed")
            return render(request,'recharge.html',{'messages':'Data integrity check failed. Please contact support.'})  
        student = request.user.student 
        existing_subscription = UserSubscription.objects.filter(uid=student).first()
        if existing_subscription:
            existing_subscription.delete()  
        
        subscription = UserSubscription(uid=student, plan=selected_plan, end_date=end_date, coins=coins,payment_id=payment['id'])
        subscription.save()
        
        return render(request,'recharge.html',{'payment':payment})

   
    if hasattr(request.user, 'student'):
        subscription = UserSubscription.objects.filter(uid=request.user.student).first()
        timeline = UserTimeline.objects.filter(uid=request.user.student).first()
        
    return render(request, 'recharge.html', {'plans': plans, 'subscription': subscription ,'timeline': timeline})

@login_required(login_url='/login') 
def success(request):
    if 'paid' in request.GET:
        paid_request = request.GET.get('paid')
        if paid_request == 'true':
            existing_subscription = UserSubscription.objects.filter(uid=request.user.student).first()
            if existing_subscription:
                existing_subscription.paid = True
            existing_subscription.save()
            return redirect('success')
    return render(request,'success.html')

@login_required(login_url='/login') 
def fail(request):
    if 'delete_request' in request.GET:
        delete_request = request.GET.get('delete_request')
        if delete_request == 'true':
            
            existing_subscription = UserSubscription.objects.filter(uid=request.user.student).first()
            if existing_subscription:
               existing_subscription.delete()
            return redirect('fail')
        
    return render(request,'fail.html')


def email_template(request):
    return render(request,'email_template.html')

@csrf_exempt  
def api(request):
    if request.method == 'POST':
        current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current_datetime = datetime.strptime(current_time_str, '%Y-%m-%d %H:%M:%S')
        current_date = current_datetime.date()
        current_date = current_date.strftime('%d/%m/%Y')
        current_time = current_datetime.time()
        print("Date:", current_date)
        print("Time:", current_time)
        rfid_tag = request.POST.get('rfid_tag').strip()
        bus_id=request.POST.get('bus_id')
        print(bus_id)
        print("rfid tag isss",rfid_tag)
        print("type is ",type(rfid_tag))
        try:
            student = get_object_or_404(Student, card_id=rfid_tag)
        except Http404:
            return JsonResponse({'message': 'No Student','user':'None'}, status=404)
        print("student",student)
        user_subscription = get_object_or_404(UserSubscription, uid=student)
        username=student.user.username.split(' ', 1)[0]
        if user_subscription.coins >= 1:
            user_subscription.coins -= 10
            user_subscription.save()

            user_timeline, created = UserTimeline.objects.get_or_create(uid=student, defaults={'timeline': []})
            timeline_entry = {
                "date": str(current_date),
                "time": str(current_time),
                "busid":bus_id,
                "balance":user_subscription.coins
            }

            if created:
                user_timeline.timeline = [timeline_entry]
                user_timeline.save()
            else:
                
                timeline_entries = user_timeline.timeline
                timeline_entries.insert(0,timeline_entry)
                user_timeline.timeline = timeline_entries
                user_timeline.save()
            
            
            return JsonResponse({'message': 'Success!!','user':username})
        else:
            return JsonResponse({'message': 'Decline!NOCoins','user':username})

    else:
       
        response_data = {'message': 'Only POST requests are allowed','user':'NONE'}
        return JsonResponse(response_data, status=400)
        









