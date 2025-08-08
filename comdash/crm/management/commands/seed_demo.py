from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from random import choice, randint, random
from datetime import timedelta

from crm.models import Campaign, Lead, Deal, Activity, Product, Quote, QuoteItem, NPSResponse


class Command(BaseCommand):
    help = "Seed demo data for quick exploration"

    def handle(self, *args, **options):
        User = get_user_model()
        user, _ = User.objects.get_or_create(username="vendedor", defaults={"email": "vendedor@example.com"})

        # Campaigns
        google, _ = Campaign.objects.get_or_create(name="Search - Marca", source="google_ads")
        fb, _ = Campaign.objects.get_or_create(name="Leads - Lookalike", source="facebook_ads")

        # Products
        p1, _ = Product.objects.get_or_create(sku="P-001", defaults={"name": "Plano Basic", "price": 199.0})
        p2, _ = Product.objects.get_or_create(sku="P-002", defaults={"name": "Plano Pro", "price": 399.0})

        # Leads + Deals
        statuses = ["new", "contacted", "qualified", "disqualified"]
        stages = ["qualification", "proposal", "negotiation", "won", "lost"]

        for i in range(40):
            camp = choice([google, fb, None])
            lead = Lead.objects.create(
                name=f"Lead {i+1}",
                email=f"lead{i+1}@example.com",
                phone=f"+55 11 9{randint(1000,9999)}-{randint(1000,9999)}",
                campaign=camp,
                status=choice(statuses),
                assigned_to=user,
                score=randint(0, 100),
            )

            if random() > 0.4:
                deal = Deal.objects.create(
                    lead=lead, stage=choice(stages), amount=choice([199, 399, 999, 1499])
                )
                # Quote
                if random() > 0.5:
                    quote = Quote.objects.create(deal=deal, status=choice(["draft", "sent", "accepted", "rejected"]))
                    for _ in range(randint(1, 3)):
                        prod = choice([p1, p2])
                        QuoteItem.objects.create(
                            quote=quote, product=prod, quantity=choice([1, 2, 3]), unit_price=prod.price
                        )
                # Activity
                Activity.objects.create(deal=deal, type=choice(["call", "email", "meeting", "followup"]))

        # Some NPS
        for i in range(15):
            NPSResponse.objects.create(
                contact_email=f"cliente{i+1}@example.com",
                score=choice(list(range(0, 11))),
                feedback=choice(["", "Ótimo atendimento!", "Poderia ser mais rápido.", "Preço alto."]),
            )

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))