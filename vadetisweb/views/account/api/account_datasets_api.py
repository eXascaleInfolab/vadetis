from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets

from vadetisweb.models import DataSet
from vadetisweb.serializers import AccountDatasetDataTablesSerializer, AccountTrainingDatasetDataTablesSerializer


class AccountDatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request information about datasets of current user
    """
    queryset = DataSet.objects.all()
    serializer_class = AccountDatasetDataTablesSerializer
    http_method_names = ['get', 'head'] # disable http put, delete etc. from ViewSet

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(owner=self.request.user, training_data=False)
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


class AccountTrainingDatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request information about datasets of current user
    """
    queryset = DataSet.objects.all()
    serializer_class = AccountTrainingDatasetDataTablesSerializer
    http_method_names = ['get', 'head'] # disable http put, delete etc. from ViewSet

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(owner=self.request.user, training_data=True)
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

