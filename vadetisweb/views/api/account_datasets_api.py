from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets

from vadetisweb.models import DataSet
from vadetisweb.utils import datatable_dataset_rows
from vadetisweb.serializers import DatasetDataTablesSerializer, TrainingDatasetDataTablesSerializer

class DatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request information about datasets of current user
    """
    queryset = DataSet.objects.all()
    serializer_class = DatasetDataTablesSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(owner=self.request.user, is_training_data=False)
        return query_set

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class TrainingDatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request information about datasets of current user
    """
    queryset = DataSet.objects.all()
    serializer_class = TrainingDatasetDataTablesSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(owner=self.request.user, is_training_data=True)
        return query_set

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

