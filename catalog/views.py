from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Product
from .serializers import ProductSerializer
from .permissions import AnonReadOnly
from .pagination import CustomPageNumberPagination

class ProductListCreateView(generics.ListCreateAPIView):
    """
    Handles listing all products and creating new ones.
    Automatically excludes soft-deleted products using the custom manager.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AnonReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["price_idr"]
    search_fields = ["name"]
    ordering_fields = ["created_at", "updated_at", "price_idr"]
    ordering = ["-created_at"]


class ProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and soft-deleting a product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AnonReadOnly]

    def destroy(self, request, *args, **kwargs):
        try:
            product = self.get_object()
            product.soft_delete()
            return Response({"message": "Product Deleted successfully."}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            response.data = {
                "access_token": response.data["access"],
                "expires_in": 3600,
                "token_type": "Bearer",
            }
        return response