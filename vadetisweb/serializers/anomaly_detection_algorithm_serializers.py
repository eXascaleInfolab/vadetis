from rest_framework import serializers
from vadetisweb.parameters import *
from vadetisweb.models import *
from vadetisweb.fields import *


class AlgorithmSerializer(serializers.Serializer):
    empty_choice = ('', '----')
    ANOMALY_DETECTION_ALGORITHMS_EMPTY = (empty_choice,) + ANOMALY_DETECTION_ALGORITHMS

    algorithm = serializers.ChoiceField(choices=ANOMALY_DETECTION_ALGORITHMS_EMPTY,
                                        required=True,
                                        help_text='The type of anomaly detection algorithm')


class HistogramSerializer(AlgorithmSerializer):
    td_selected = TrainingDatasetField(label='Training Dataset',
                                       queryset=DataSet.objects.none(),
                                       empty_label="----", )

    train_size = TrainSizeFloatField(min_value=0.001, max_value=0.999, required=True)

    random_seed = RandomSeedIntegerField(required=False)

    time_range = TimeRangeChoiceField(required=True)

    maximize_score = MaximizeScoreChoiceField(required=True)

    range_start = serializers.IntegerField(required=True, min_value=0, widget=serializers.HiddenField())
    range_end = serializers.IntegerField(required=True, min_value=0, widget=serializers.HiddenField())

    def __init__(self, *args, **kwargs):
        post_data = args[0]
        super(HistogramSerializer, self).__init__(*args, **kwargs)
        training_datasets = DataSet.objects.filter(original_dataset__id=post_data['dataset_selected'],
                                                   is_training_data=True)
        self.fields['td_selected'].queryset = training_datasets

    def validate_td_selected(self):
        data = self.validated_data.get('td_selected', None)
        if not data:
            raise serializers.ValidationError('This field is required.')
        else:
            data = data.id
        return data


class ClusterSerializer(AlgorithmSerializer):
    td_selected = TrainingDatasetField(label='Training Dataset',
                                       queryset=DataSet.objects.none(),
                                       empty_label="----", )

    n_components = serializers.IntegerField(label='Number of Components', min_value=1, required=True,
                                            help_text='The number of mixture components.',
                                            style={'template': 'vadetisweb/parts/input/text_input.html'})

    n_init = serializers.IntegerField(label='Number of Inits', min_value=1, required=True,
                                      help_text='The number of initializations to perform. The best results are kept.',
                                      style={'template': 'vadetisweb/parts/input/text_input.html'})

    train_size = TrainSizeFloatField(min_value=0.001, max_value=0.999, required=True)

    random_seed = RandomSeedIntegerField(required=False)

    time_range = TimeRangeChoiceField(required=True)

    maximize_score = MaximizeScoreChoiceField(required=True)

    range_start = serializers.IntegerField(required=True, min_value=0, widget=serializers.HiddenField())
    range_end = serializers.IntegerField(required=True, min_value=0, widget=serializers.HiddenField())

    def __init__(self, *args, **kwargs):
        post_data = args[0]
        super(ClusterSerializer, self).__init__(*args, **kwargs)

        training_datasets = DataSet.objects.filter(original_dataset__id=post_data['dataset_selected'],
                                                   is_training_data=True)
        self.fields['td_selected'].queryset = training_datasets

    def validate_td_selected(self):
        data = self.validated_data.get('td_selected', None)
        if not data:
            raise serializers.ValidationError('This field is required.')
        else:
            data = data.id
        return data


class SVMSerializer(AlgorithmSerializer):
    td_selected = TrainingDatasetField(label='Training Dataset',
                                       queryset=DataSet.objects.none(),
                                       empty_label="----", )

    kernel = serializers.ChoiceField(label='Kernel', choices=SVM_KERNELS, required=True,
                                     help_text='The kernel for the SVM.',
                                     style={'template': 'vadetisweb/parts/input/select_input.html'})

    gamma = serializers.FloatField(label='Gamma', min_value=0.00000001, max_value=1, required=False,
                                   help_text='Kernel coefficient for \'rbf\', \'poly\' and \'sigmoid\'; ignored for \'linear\' kernel. The optimal value depends entirely on the data. If gamma is \'None\' then (1 / Number of features) will be used instead.',
                                   style={'template': 'vadetisweb/parts/input/text_input.html'})

    nu = serializers.FloatField(label='Nu', min_value=0.000001, max_value=1, required=False,
                                help_text='An upper bound on the fraction of training errors and a lower bound of the fraction of support vectors. Should be in the interval (0, 1]. If none, the default value 0.5 will be used.',
                                style={'template': 'vadetisweb/parts/input/text_input.html'})

    train_size = TrainSizeFloatField(min_value=0.001, max_value=0.999, required=True)

    random_seed = RandomSeedIntegerField(required=False)

    time_range = TimeRangeChoiceField(required=True)

    maximize_score = MaximizeScoreChoiceField(required=True)

    range_start = serializers.IntegerField(required=True, min_value=0, widget=serializers.HiddenField())
    range_end = serializers.IntegerField(required=True, min_value=0, widget=serializers.HiddenField())

    def __init__(self, *args, **kwargs):
        post_data = args[0]
        super(SVMSerializer, self).__init__(*args, **kwargs)

        training_datasets = DataSet.objects.filter(original_dataset__id=post_data['dataset_selected'],
                                                   is_training_data=True)
        self.fields['td_selected'].queryset = training_datasets

    def validate_td_selected(self):
        data = self.validated_data.get('td_selected', None)
        if not data:
            raise serializers.ValidationError('This field is required.')
        else:
            data = data.id
        return data


class IsolationForestSerializer(AlgorithmSerializer):
    td_selected = TrainingDatasetField(label='Training Dataset',
                                       queryset=DataSet.objects.none(),
                                       empty_label="----", )

    bootstrap = serializers.BooleanField(label='Bootstrap', required=False,
                                         help_text='If True, individual trees are fit on random subsets of the training data sampled with replacement. If False, sampling without replacement is performed.',
                                         style={'template': 'vadetisweb/parts/input/select_input.html'})

    n_estimators = serializers.IntegerField(label='Number of Estimators', min_value=1, required=True,
                                            help_text='The number of base estimators in the ensemble.',
                                            style={'template': 'vadetisweb/parts/input/text_input.html'})

    train_size = TrainSizeFloatField(min_value=0.001, max_value=0.999, required=True)

    random_seed = RandomSeedIntegerField(required=False)

    time_range = TimeRangeChoiceField(required=True)

    maximize_score = MaximizeScoreChoiceField(required=True)

    range_start = serializers.IntegerField(required=True, min_value=0, widget=serializers.HiddenField())
    range_end = serializers.IntegerField(required=True, min_value=0, widget=serializers.HiddenField())

    def __init__(self, *args, **kwargs):
        post_data = args[0]
        super(IsolationForestSerializer, self).__init__(*args, **kwargs)
        training_datasets = DataSet.objects.filter(original_dataset__id=post_data['dataset_selected'],
                                                   is_training_data=True)
        self.fields['td_selected'].queryset = training_datasets

    def validate_td_selected(self):
        data = self.validated_data.get('td_selected', None)
        if not data:
            raise serializers.ValidationError('This field is required.')
        else:
            data = data.id
        return data
