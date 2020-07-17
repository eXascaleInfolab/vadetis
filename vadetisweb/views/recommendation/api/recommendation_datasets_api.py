from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from vadetisweb.serializers.dataset.recommendation_dataset_serializer import *
from vadetisweb.utils import q_shared_or_user_is_owner


class RecommendationSyntheticDatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request synthetic datasets
    """
    queryset = DataSet.objects.all()
    serializer_class = RecommendationDatasetDataTablesSerializer
    http_method_names = ['get', 'head'] # disable http put, delete etc. from ViewSet

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(Q(type=SYNTHETIC, training_data=False),
                                    q_shared_or_user_is_owner(self.request))
        return query_set

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class RecommendationRealWorldDatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request real-world datasets
    """
    queryset = DataSet.objects.all()
    serializer_class = RecommendationDatasetDataTablesSerializer
    http_method_names = ['get', 'head'] # disable http put, delete etc. from ViewSet

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(Q(type=REAL_WORLD, training_data=False),
                                    q_shared_or_user_is_owner(self.request))
        return query_set

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]