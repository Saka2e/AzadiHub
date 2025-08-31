from rest_framework import serializers
from crawler.models import Config

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = '__all__'