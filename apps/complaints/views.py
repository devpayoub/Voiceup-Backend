from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Company, Complaint, ComplaintBacker, Region, StatusHistory
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    CompanySerializer,
    ComplaintSerializer,
    RegionSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class ComplaintViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = Complaint.objects.select_related('company', 'category', 'user').prefetch_related('backers')
        params = self.request.query_params
        for field in ('category', 'company', 'region', 'status'):
            value = params.get(field)
            if value:
                qs = qs.filter(**{field: value})
        search = params.get('search')
        if search:
            qs = qs.filter(title__icontains=search)
        return qs

    def get_serializer_context(self):
        return {**super().get_serializer_context(), 'request': self.request}

    def perform_create(self, serializer):
        complaint = serializer.save(user=self.request.user)
        StatusHistory.objects.create(
            complaint=complaint, status=complaint.status, changed_by=self.request.user
        )

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def back(self, request, pk=None):
        complaint = self.get_object()
        backing, created = ComplaintBacker.objects.get_or_create(complaint=complaint, user=request.user)
        if not created:
            backing.delete()
        backer_count = ComplaintBacker.objects.filter(complaint=complaint).count()
        return Response({'backed': created, 'backer_count': backer_count})

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def comments(self, request, pk=None):
        complaint = self.get_object()
        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, complaint=complaint)
            return Response(serializer.data, status=201)
        serializer = CommentSerializer(complaint.comments.all(), many=True)
        return Response(serializer.data)
