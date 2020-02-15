from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets

from vadetisweb.models import DataSet
from vadetisweb.utils import datatable_dataset_rows
from vadetisweb.serializers import DatasetDataTablesSerializer

class DatasetDataTableViewSet(viewsets.ModelViewSet):
    """
    Request information about datasets of current user
    """
    queryset = DataSet.objects.all()
    serializer_class = DatasetDataTablesSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(owner=self.request.user)
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


class AccountTrainingDatasetsJson(APIView):
    """
    Request information about datasets of current user
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        user = request.user
        data = []

        datasets = DataSet.objects.filter(owner=user, is_training_data=True)
        data = datatable_dataset_rows(data, datasets)

        return Response(data)

