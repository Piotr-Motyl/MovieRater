from django.contrib.auth.models import User
from rest_framework import serializers
from .models import AdditionalInfo, Review, Movie

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data) #haszowanie hasla dla usera
        return user

class AdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.review_description = validated_data.get('review_description', instance.review_description)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()

        return instance

class MovieSerializer(serializers.ModelSerializer):
    additional_info = AdditionalInfoSerializer(many=False, required=False)
    reviews = ReviewSerializer(many=True, required=False)

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('additional_info', 'reviews')
