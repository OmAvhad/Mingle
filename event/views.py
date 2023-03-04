from django.shortcuts import render
from .serializers import *
from django.http import JsonResponse
# Create your views here.
from UserAccounts.models import *

from django.db import transaction
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

from datetime import datetime
from fuzzywuzzy import fuzz


# @transaction.atomic
# @login_required
@api_view(['POST'])
def addEvent(request):
    data = request.data 
    user_id = request.query_params.get('id')
    user = CustomUser.objects.filter(id=user_id).last()
    query_set = Events.objects.filter(user__id=data.get('id'),event_name=data.get('event_name'))
    if query_set.exists():
        return JsonResponse({"message":"Event Already Added"})
    else:
        if user.user_type=="organizer":
            serializer = EventSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"msg":"New Event is Added"})
            else:
                print(serializer.errors)
                return JsonResponse({"msg":"User Does not Match"})
        

@api_view(['GET'])
def getEventListOrg(request):
    user_id = request.query_params.get('id')
    queryset = Events.objects.filter(user=user_id)
    serialized_data = EventSerializer(queryset,many=True).data
    return JsonResponse({"data":serialized_data})

#Showing Upcoming hackathon
@api_view(['GET'])
def getEventList(request):
    event = Events.objects.filter(date__gte=datetime.now())
    data = EventSerializer(event,many=True).data
    return JsonResponse({"msg":"upcoming hackathon","data":data})

#Adding Rating
@api_view(['POST'])
def addRating(request):
    data = request.data 
    user_id = request.query_params.get('user_id')
    data['event'] = Events.objects.filter(id = request.data.get('event_id'))
    user = CustomUser.objects.filter(id=user_id).last()
    if Rate.objects.filter(description=data.get('description'),event=data['event']).exists():
        return JsonResponse({"msg":"Rating Already exists. "})
    else:
        if user.user_type=="user":
            serializer = RateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"msg":"New Rating is Added"})
            else:
                return JsonResponse({"msg":"User Does not Match"})
        else:
            return JsonResponse({"msg":"Invalid User"})
##Get Particular Event
@api_view(['GET'])
def getEvent(request):
    id = request.query_params.get('id')
    event = Events.objects.filter(id=id)
    if event!=None:
        return JsonResponse({"data":list(event.values())})
    else:
        return JsonResponse({"msg":"No Such Event Found"})

#Register For Event 

@api_view(['POST'])
def registerForEvent(request):
    event_id = request.query_params.get('event_id')
    user_id = request.query_params.get('user_id')
    # tb = UserAppliedforEvents.objects.filter().last()
    # tb.delete()
    user_applied_for = UserAppliedforEvents.objects
    if user_applied_for.filter(event=event_id,user__id=user_id).exists():
        return JsonResponse({"message":"Registration already Done!"})
    else:
        event = Events.objects.filter(id=event_id).last()
        user = CustomUser.objects.filter(id=user_id).last()
        print("user:",user)

    #Creating Connection
        createConnection(request,event_id)

        UserAppliedforEvents.objects.create(user=user,event=event)
        return JsonResponse({"message":"Registeration is Done"})

@api_view(['GET'])
def getRegisterData(request):
    event_id = request.query_params.get('event_id')
    queryset = UserAppliedforEvents.objects.filter(event_id=event_id)
    data = UserAppliedforEventsSerializer(queryset,many=True).data
    return JsonResponse({"data":data})


def createConnection(request,event_id):
    
    user_id = request.query_params.get('user_id')

    interest = CustomUser.objects.filter(id=user_id).first().interests
    u_id = UserAppliedforEvents.objects.filter(event__id=event_id).values_list('user__id')

    temp = CustomUser.objects.filter(id__in=u_id,interests__contains=['girls','boys']) 
    print("temp ::: ", temp)

    temp_list = []
    for i in interest:
        
        t = CustomUser.objects.filter(id__in=u_id,interests__icontains=i)     
       
        temp_list.append(t)
    
    qs = temp_list[0]
    
    # temp_list = [x for x in temp_list if x is not None]
    print("temp_list",temp_list)

    for t in range(len(temp_list) - 1):
        qs = qs.union(temp_list[t+1])
    
    print("qs :: ", qs)
    
    ftl = []

    for q in qs:

        inrts = q.interests

        test_list = []
        for i in interest:
            for p in inrts:
                test_list.append(fuzz.ratio(i, p))

        ftl.append(sum(test_list))
        
    
    m = max(ftl)
    mi = ftl.index(m)

    print("final :: ", qs[mi])
    Match.objects.create(user_1_id=u_id,user_2_id=)        



def create_event(request):
    return render(request, 'events/create_event.html')
