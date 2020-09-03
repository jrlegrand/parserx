from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sig import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'sig', views.SigViewSet)
router.register(r'bulk_sig', views.BulkSigCreateViewSet)
router.register(r'csv_sig', views.CsvSigCreateViewSet)
router.register(r'sig_reviewed', views.SigReviewedViewSet)
router.register(r'user', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]