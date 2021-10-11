from rest_framework import serializers
from .models import Announcement,Announce_type
from personality.models import User,Location,Metro,City

class AnnounceSerializer(serializers.ModelSerializer):
    user_pk = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True)
    type_pk=serializers.PrimaryKeyRelatedField(
        queryset=Announce_type.objects.all(), source='type', write_only=True)
    class Meta:
        model = Announcement
        fields = '__all__'
        depth= 2
