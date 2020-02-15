from rest_framework import serializers
from vadetisweb.models import DataSet

class UserOriginalDatasetField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        user = request.user
        return DataSet.objects.filter(owner=user, is_training_data=False)

    def display_value(self, instance):
        return instance.title
