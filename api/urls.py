from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'company', views.CompanyViewSet)
router.register(r'site', views.SiteViewSet)
router.register(r'position', views.PositionViewSet)
router.register(r'department', views.DepartmentViewSet)

urlpatterns = [
  path('auth/', include('djoser.urls')),
  path('', include(router.urls)),
]
