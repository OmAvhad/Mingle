from django.shortcuts import render
from .serializers import *
from django.http import JsonResponse
# Create your views here.
from UserAccounts.models import *

from django.db import transaction
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

from datetime import datetime
# @transaction.atomic
# @login_required
@api_view(['POST'])
def addEvent(request):
    data = request.data 
    user_id = request.query_params.get('id')
    user = CustomUser.objects.filter(id=user_id).last()
    query_set = Events.objects.filter(email=data.get('email'),event_name=data.get('event_name'))
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

def getEventListUser(request):
    
    user_id = request.query_params.get('id')
    queryset = Events.objects.filter(user=user_id)
    
    serialized_data = EventSerializer(queryset,many=True).data
    return JsonResponse({"data":serialized_data})

#Showing Upcoming hackathon
@api_view(['GET'])
def getEventListUser(request):
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
    user_applied_for = UserAppliedforEvents.objects
    if user_applied_for.filter(event=event_id).exists():
        return JsonResponse({"message":"Registration already Done!"})
    else:
        event = Events.objects.filter(id=event_id).last()
        user = CustomUser.objects.filter(id=user_id).last()
        print("user:",user)

    #Creating Connection
        createConnection(request)

        UserAppliedforEvents.objects.create(user=user,event=event)
        return JsonResponse({"message":"Registeration is Done"})

@api_view(['GET'])
def getRegisterData(request):
    event_id = request.query_params.get('event_id')
    queryset = UserAppliedforEvents.objects.filter(event_id=event_id)
    data = UserAppliedforEventsSerializer(queryset,many=True).data
    return JsonResponse({"data":data})


def createConnection(request):

    CustomUser.objects.filter(user)
    


