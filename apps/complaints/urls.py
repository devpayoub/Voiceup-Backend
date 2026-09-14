from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, CompanyViewSet, ComplaintViewSet, RegionViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('companies', CompanyViewSet, basename='company')
router.register('regions', RegionViewSet, basename='region')
router.register('complaints', ComplaintViewSet, basename='complaint')

urlpatterns = router.urls
