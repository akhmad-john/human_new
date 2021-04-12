from rest_framework import serializers
from .models import *

class AdDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('id', 'banner', 'ad_type', )