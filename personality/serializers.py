from rest_framework import serializers
from .models import User,Location,Metro,City
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
    def validate(self, data):
        if 'city' in data:
            try:
                data['city']=City.objects.get(city=data['city'])
            except:
                raise serializers.ValidationError("we don`t have this city in our list")
        else:
            data['city']=self.city
        if 'metro' in data:
            try:
                data['metro']=Metro.objects.get(station=data['metro'],city=data['city'])
            except Exception as e:
                raise serializers.ValidationError("wrong station"+str(e))
        return data
    def create(self, validated_data):
        return Location.objects.create(**validated_data)
    def update(self, instance, validated_data):

        instance.metro=validated_data.get('metro', instance.metro)
        instance.city=validated_data.get('city', instance.city)
        instance.street=validated_data.get('street', instance.street)
        instance.house=validated_data.get('home', instance.house)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    #location=LocationSerializer()
    location_pk = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='location', write_only=True)
    class Meta:
        model = User
        fields = '__all__'
        depth = 1
    def validate_phone(self, value):
        if len(str(value))!=11:
            raise serializers.ValidationError("Lenght of phone is wrong")
        if str(value)[0]!='8' and str(value)[0]!='7':
            raise serializers.ValidationError("We dont support not russian phones")
        return value
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.location=validated_data.get('location', instance.location)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance
    def create(self,validated_data):
        print(validated_data)
        data={'email':validated_data['email'], 'phone':validated_data['phone'], 'password':validated_data['password']}
        us=User.objects.create_user(**data)
        us.location=validated_data['location']
        us.save()
        return us
class AuthSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=200)
    password=serializers.CharField(max_length=200)
