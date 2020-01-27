from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class SyntheticDatasets(APIView):
    """
    View for synthetic datasets
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/datasets/synthetic/datasets.html'

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class RealWorldDatasets(APIView):
    """
    View for real world datasets
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/datasets/real-world/datasets.html'

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class SyntheticDataset(APIView):
    """
    View for a single synthetic dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/datasets/synthetic/dataset.html'

    def get(self, request, dataset_id):
        return Response(status=status.HTTP_200_OK)


class RealWorldDataset(APIView):
    """
    View for a single real world dataset
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vadetisweb/datasets/real-world/dataset.html'

    def get(self, request, dataset_id):
        return Response(status=status.HTTP_200_OK)
