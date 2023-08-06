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
from django.urls import include, path

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'part', views.PartViewSet)
router.register(r'vendor', views.VendorViewSet)
router.register(r'vendor_part', views.VendorPartViewSet)
router.register(r'assembly_item', views.AssemblyItemViewSet)

urlpatterns = [
    path('', include(router.urls))
]
