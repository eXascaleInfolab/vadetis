from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import viewsets

from vadetisweb.models import DataSet
from vadetisweb.parameters import REAL_WORLD, SYNTHETIC
from vadetisweb.serializers import DetectionDatasetDataTablesSerializer

class DetectionSyntheticDatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request synthetic datasets
    """
    queryset = DataSet.objects.all()
    serializer_class = DetectionDatasetDataTablesSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(type=SYNTHETIC, is_public=True, is_training_data=False)
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


class DetectionRealWorldDatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request real-world datasets
    """
    queryset = DataSet.objects.all()
    serializer_class = DetectionDatasetDataTablesSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(type=REAL_WORLD, is_public=True, is_training_data=False)
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