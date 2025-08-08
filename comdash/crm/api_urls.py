from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CampaignViewSet,
    LeadViewSet,
    DealViewSet,
    ActivityViewSet,
    ProductViewSet,
    QuoteViewSet,
    QuoteItemViewSet,
    NPSResponseViewSet,
    metrics_summary,
)

router = DefaultRouter()
router.register(r"campaigns", CampaignViewSet)
router.register(r"leads", LeadViewSet)
router.register(r"deals", DealViewSet)
router.register(r"activities", ActivityViewSet)
router.register(r"products", ProductViewSet)
router.register(r"quotes", QuoteViewSet)
router.register(r"quote-items", QuoteItemViewSet)
router.register(r"nps", NPSResponseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("metrics/summary/", metrics_summary, name="metrics-summary"),
]