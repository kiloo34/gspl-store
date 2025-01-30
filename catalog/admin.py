from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price_idr","price_sgd", "created_at", "updated_at", "deleted_at")
    list_filter = ("created_at", "updated_at", "price_idr", "price_sgd")
    search_fields = ("name",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"

    actions = ["soft_delete_products", "restore_products"]

    def soft_delete_products(self, request, queryset):
        queryset.update(deleted_at=now())
        self.message_user(request, "Produk berhasil dihapus (soft delete).")

    def restore_products(self, request, queryset):
        queryset.update(deleted_at=None)
        self.message_user(request, "Produk berhasil dipulihkan.")

    soft_delete_products.short_description = "Soft delete produk yang dipilih"
    restore_products.short_description = "Pulihkan produk yang dipilih"
