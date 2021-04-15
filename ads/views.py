from django.shortcuts import render
from .models import Advertisement
from rest_framework import status, viewsets, filters
from rest_framework import generics
from .serializers import AdDisplaySerializer
import random
from itertools import chain

# Create your views here.

class AdDisplayView(generics.ListAPIView):
    queryset = Advertisement.objects.filter(active=True)
    serializer_class = AdDisplaySerializer

    def get_queryset(self):
        # up
        # ads_up_base = self.queryset.filter(ad_type=1)
        # ads_up_ids = ads_up_base.values_list('id', flat=True)
        # ads_up_random = random.sample(list(ads_up_ids), 2)
        # ads_up = ads_up_base.filter(id__in=ads_up_random)

        # side
        ads_side_base = self.queryset.filter(ad_type=2)
        ads_side_ids = ads_side_base.values_list('id', flat=True)
        ads_side_random = random.sample(list(ads_side_ids), 1)
        ads_side = ads_side_base.filter(id__in=ads_side_random)

        # bottom
        ads_bottom_base = self.queryset.filter(ad_type=3)
        ads_bottom_ids = ads_bottom_base.values_list('id', flat=True)
        ads_bottom_random = random.sample(list(ads_bottom_ids), 1)
        ads_bottom = ads_bottom_base.filter(id__in=ads_bottom_random)

        # append ads
        final_list = list(chain(ads_side, ads_bottom))
        print(ads_side)
        return final_list
