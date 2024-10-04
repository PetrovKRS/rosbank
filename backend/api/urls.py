from django.urls import include, path, re_path
from rest_framework import routers

from api.views import (
WorkersViewSet
)

router_v1 = routers.DefaultRouter()


router_v1.register(r'workers/list', WorkersViewSet, basename='workers')
# router_v1.register(r'products', ProductListViewSet, basename='product')
# router_v1.register(r'outfit', ProductDetailViewSet, basename='outfit')
# router_v1.register(r'shopping', ShoppingViewSet, basename='shopping')




urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('auth/', include('djoser.urls')),
    # re_path('auth/', include('djoser.urls.authtoken')),
]