
from event.models import *
from rest_framework import serializers
from UserAccounts.models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'
        
class UserAppliedforEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAppliedforEvents
        fields = '__all__'
        
class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'
        