#
#   Copyright (c) 2021 eGauge Systems LLC
# 	1644 Conestoga St, Suite 2
# 	Boulder, CO 80301
# 	voice: 720-545-9767
# 	email: davidm@egauge.net
#
#   All rights reserved.
#
#   This code is the property of eGauge Systems LLC and may not be
#   copied, modified, or disclosed without any prior and written
#   permission from eGauge Systems LLC.
#
# PYLINT: disable=too-few-public-methods, no-member
import django_filters.rest_framework

from rest_framework import permissions, serializers, viewsets

from epic.models import Assembly_Item, Part, Vendor, Vendor_Part
from epic.perms import VIEW, EDIT

from django.contrib.auth.models import Permission

class IsAuthorized(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.has_perms((VIEW,))
        return request.user.has_perms((EDIT,))

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class VendorPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Part
        fields = '__all__'

class AssemblyItemPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assembly_Item
        fields = '__all__'

class PartViewSet(viewsets.ModelViewSet):
    '''API endpoint for viewing and editing parts.'''
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAuthorized]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['val', 'mfg', 'mfg_pn', 'mounting', 'status']

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthorized]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name']

class VendorPartViewSet(viewsets.ModelViewSet):
    queryset = Vendor_Part.objects.all()
    serializer_class = VendorPartSerializer
    permission_classes = [IsAuthorized]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['part', 'vendor', 'vendor_pn', 'status']

class AssemblyItemViewSet(viewsets.ModelViewSet):
    queryset = Assembly_Item.objects.all()
    serializer_class = AssemblyItemPartSerializer
    permission_classes = [IsAuthorized]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['assy', 'comp', 'qty', 'refdes']
