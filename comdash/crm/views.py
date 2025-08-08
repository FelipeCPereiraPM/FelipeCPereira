from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q, Avg
from rest_framework import viewsets, permissions, response, decorators

from .models import Campaign, Lead, Deal, Activity, Product, Quote, QuoteItem, NPSResponse
from .serializers import (
    CampaignSerializer,
    LeadSerializer,
    DealSerializer,
    ActivitySerializer,
    ProductSerializer,
    QuoteSerializer,
    QuoteItemSerializer,
    NPSResponseSerializer,
)


class IsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    pass


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all().order_by("name")
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ["source"]
    search_fields = ["name", "external_id"]


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by("-created_at")
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ["status", "campaign", "assigned_to"]
    search_fields = ["name", "email", "phone"]


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all().order_by("-created_at")
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ["stage", "lead"]


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all().order_by("-created_at")
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ["type", "completed", "lead", "deal"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("name")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ["name", "sku"]


class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all().order_by("-created_at")
    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ["status", "deal"]


class QuoteItemViewSet(viewsets.ModelViewSet):
    queryset = QuoteItem.objects.all()
    serializer_class = QuoteItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class NPSResponseViewSet(viewsets.ModelViewSet):
    queryset = NPSResponse.objects.all().order_by("-created_at")
    serializer_class = NPSResponseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ["score", "deal"]


@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.AllowAny])
def metrics_summary(request):
    now = timezone.now()
    last_30_days = now - timedelta(days=30)

    leads_total = Lead.objects.count()
    leads_last_30 = Lead.objects.filter(created_at__gte=last_30_days).count()

    deals_total = Deal.objects.count()
    deals_won = Deal.objects.filter(stage="won").count()
    deals_lost = Deal.objects.filter(stage="lost").count()

    avg_deal_amount = Deal.objects.aggregate(avg=Avg("amount")).get("avg") if deals_total else 0

    # Conversion rates
    qualified = Lead.objects.filter(status="qualified").count()
    conversion_lead_to_qualified = (qualified / leads_total) * 100 if leads_total else 0
    won_pct = (deals_won / deals_total) * 100 if deals_total else 0

    nps_count = NPSResponse.objects.count()
    promoters = NPSResponse.objects.filter(score__gte=9).count()
    detractors = NPSResponse.objects.filter(score__lte=6).count()
    nps = ((promoters - detractors) / nps_count) * 100 if nps_count else 0

    data = {
        "leads_total": leads_total,
        "leads_last_30": leads_last_30,
        "deals_total": deals_total,
        "deals_won": deals_won,
        "deals_lost": deals_lost,
        "avg_deal_amount": float(avg_deal_amount) if avg_deal_amount else 0,
        "conversion_lead_to_qualified_pct": round(conversion_lead_to_qualified, 2),
        "win_rate_pct": round(won_pct, 2),
        "nps": round(nps, 2),
        "by_stage": list(
            Deal.objects.values("stage").annotate(total=Count("id")).order_by("stage")
        ),
        "leads_by_status": list(
            Lead.objects.values("status").annotate(total=Count("id")).order_by("status")
        ),
    }

    return response.Response(data)