from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import viewsets

from django.db.models import Q

from vadetisweb.models import DataSet
from vadetisweb.parameters import REAL_WORLD, SYNTHETIC
from vadetisweb.serializers.dataset.display_dataset_serializer import *
from vadetisweb.utils import q_public_or_user_is_owner

class DisplaySyntheticDatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request synthetic datasets
    """
    queryset = DataSet.objects.all()
    serializer_class = DisplayDatasetDataTablesSerializer
    http_method_names = ['get', 'head'] # disable http put, delete etc. from ViewSet

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(Q(type=SYNTHETIC, training_data=False),
                                    q_public_or_user_is_owner(self.request))
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


class DisplayRealWorldDatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request real-world datasets
    """
    queryset = DataSet.objects.all()
    serializer_class = DisplayDatasetDataTablesSerializer
    http_method_names = ['get', 'head'] # disable http put, delete etc. from ViewSet

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(Q(type=REAL_WORLD, training_data=False),
                                    q_public_or_user_is_owner(self.request))
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


class DisplayTrainingDatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request training datasets of a main dataset by query param
    """
    queryset = DataSet.objects.all()
    serializer_class = DisplayTrainingDatasetDataTablesSerializer
    http_method_names = ['get', 'head'] # disable http put, delete etc. from ViewSet

    def get_queryset(self):
        queryset = self.queryset
        main_dataset_id = self.request.query_params.get('main', None)
        if main_dataset_id is not None:
            query_set = queryset.filter(Q(main_dataset_id=main_dataset_id, training_data=True),
                                        q_public_or_user_is_owner(self.request))
        else:
            query_set = queryset.filter(Q(training_data=True),
                                        q_public_or_user_is_owner(self.request))
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