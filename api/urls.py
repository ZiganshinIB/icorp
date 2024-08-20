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
  # get: /api/ad/user/?username=username view = views.get_ADUser,
  # post: /api/ad/user/ view = views.create_ADUser
  # delete: /api/ad/user/ view = views.delete_ADUser
  # put: /api/ad/user/ view = views.update_ADUser
  path('ad/user/', views.ADUserViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
  })),

]
