from __future__ import absolute_import

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ..models import UserProfile, UserVerify

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=255, min_length=6, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, max_length=255, min_length=6, required=True)
    first_name = serializers.CharField(max_length=255, min_length=2)
    middle_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)
    email = serializers.EmailField(max_length=255, min_length=2, required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ["first_name", "middle_name", "last_name", "email", "username", "password", "password2", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email', ('Email is already in use!')})

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            middle_name=validated_data['middle_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        # user_profile = Profile.objects.create(user=user, username=username) # if there was a profile model with one to one relationship with the django user model
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault)

    class Meta:
        model = UserProfile
        fields = ['user', 'passport', 'bank', 'account_no', 'routing_no', 'nationality', 'phone', 'url']
        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
            "user": {"read_only":True, "required":True}
        }

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of user profile
        :return: returns a successfully created profile record
        """
        profile, created = UserProfile.objects.update_or_create(
            user=self.context['request'].user, 
            passport=validated_data['passport'],
            bank=validated_data['bank'],
            account_no=validated_data['account_no'],
            routing_no=validated_data['routing_no'],
            nationality=validated_data['nationality'],
            phone=validated_data['phone'],
        )
        return profile


class UserVerifySerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault)
    
    class Meta:
        model = UserVerify
        fields = ['user', 'id_type', 'id_front', 'id_back', 'bank_statement', 'ssn', 'url']
        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
            "user": {"read_only":True, "required":True}
        }

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of user profile
        :return: returns a successfully created profile record
        """
        verify, created = UserVerify.objects.update_or_create(
            user=self.context['request'].user, 
            id_type=validated_data['id_type'],
            id_front=validated_data['id_front'],
            id_back=validated_data['id_back'],
            bank_statement=validated_data['bank_statement'],
            ssn=validated_data['ssn'],
        )
        return verify


        