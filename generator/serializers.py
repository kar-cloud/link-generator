from rest_framework import serializers
from .models import Link, Analytics


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'

    def create(self, validated_data):
        link_instance = Link.objects.create(**validated_data)
        Analytics.objects.create(link_id=link_instance.id)
        return link_instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            analytics_obj = Analytics.objects.get(link_id=instance.id)
            analytics_data = {
                'no_of_clicks': analytics_obj.no_of_clicks,
                'no_of_unique_viewers': analytics_obj.no_of_unique_viewers
            }
        except:
            analytics_data = None
        representation['analytics'] = analytics_data
        return representation
