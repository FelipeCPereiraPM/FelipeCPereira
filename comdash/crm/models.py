from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Campaign(models.Model):
    SOURCE_CHOICES = [
        ("google_ads", "Google Ads"),
        ("facebook_ads", "Facebook Ads"),
        ("organic", "Orgânico"),
        ("other", "Outro"),
    ]

    name = models.CharField(max_length=255)
    external_id = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default="google_ads")
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.get_source_display()})"


class Lead(models.Model):
    STATUS_CHOICES = [
        ("new", "Novo"),
        ("contacted", "Contactado"),
        ("qualified", "Qualificado"),
        ("disqualified", "Desqualificado"),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name="leads")
    source = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_leads")
    score = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.status})"


class Deal(models.Model):
    STAGE_CHOICES = [
        ("qualification", "Qualificação"),
        ("proposal", "Proposta"),
        ("negotiation", "Negociação"),
        ("won", "Ganho"),
        ("lost", "Perdido"),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="deals")
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default="qualification")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    expected_close_date = models.DateField(blank=True, null=True)
    close_date = models.DateField(blank=True, null=True)
    loss_reason = models.CharField(max_length=255, blank=True, null=True)
    probability = models.PositiveSmallIntegerField(default=10)

    def __str__(self) -> str:
        return f"Deal #{self.id} - {self.lead.name} ({self.stage})"


class Activity(models.Model):
    TYPE_CHOICES = [
        ("call", "Ligação"),
        ("email", "Email"),
        ("meeting", "Reunião"),
        ("followup", "Follow-up"),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="activities", null=True, blank=True)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="activities", null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    due_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="activities_created")

    def __str__(self) -> str:
        target = self.deal or self.lead
        return f"{self.get_type_display()} - {target}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.sku} - {self.name}"


class Quote(models.Model):
    STATUS_CHOICES = [
        ("draft", "Rascunho"),
        ("sent", "Enviado"),
        ("accepted", "Aceito"),
        ("rejected", "Rejeitado"),
    ]

    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sent_at = models.DateTimeField(blank=True, null=True)
    accepted_at = models.DateTimeField(blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"Quote #{self.id} - {self.deal} ({self.status})"


class QuoteItem(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    def line_total(self):
        return self.quantity * self.unit_price


class NPSResponse(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    contact_email = models.EmailField()
    score = models.PositiveSmallIntegerField()
    feedback = models.TextField(blank=True, null=True)
    deal = models.ForeignKey(Deal, on_delete=models.SET_NULL, null=True, blank=True, related_name="nps_responses")

    def __str__(self) -> str:
        return f"NPS {self.score} - {self.contact_email}"