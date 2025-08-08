from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q

from .models import Lead, Deal


def get_basic_counts(days: int = 30):
    now = timezone.now()
    window = now - timedelta(days=days)

    return {
        "leads_total": Lead.objects.count(),
        "leads_window": Lead.objects.filter(created_at__gte=window).count(),
        "deals": Deal.objects.aggregate(
            total=Count("id"),
            won=Count("id", filter=Q(stage="won")),
            lost=Count("id", filter=Q(stage="lost")),
        ),
    }