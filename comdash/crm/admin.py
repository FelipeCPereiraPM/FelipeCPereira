from django.contrib import admin
from .models import Campaign, Lead, Deal, Activity, Product, Quote, QuoteItem, NPSResponse


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("name", "source", "budget", "start_date", "end_date")
    search_fields = ("name", "external_id")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "status", "campaign", "assigned_to", "created_at")
    list_filter = ("status", "campaign", "assigned_to")
    search_fields = ("name", "email", "phone")


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ("id", "lead", "stage", "amount", "expected_close_date", "close_date")
    list_filter = ("stage",)
    search_fields = ("lead__name",)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("type", "lead", "deal", "due_date", "completed")
    list_filter = ("type", "completed")


class QuoteItemInline(admin.TabularInline):
    model = QuoteItem
    extra = 1


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("id", "deal", "status", "total_amount", "created_at")
    list_filter = ("status",)
    inlines = [QuoteItemInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "price")
    search_fields = ("sku", "name")


@admin.register(NPSResponse)
class NPSResponseAdmin(admin.ModelAdmin):
    list_display = ("contact_email", "score", "deal", "created_at")
    list_filter = ("score",)