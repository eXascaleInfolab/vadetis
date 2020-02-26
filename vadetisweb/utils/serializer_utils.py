
from vadetisweb.serializers import TSSerializer, CorrelationSerializer, PearsonSerializer, DTWPearsonSerializer, GeographicDistanceSerializer
from vadetisweb.parameters import PEARSON, DTW, GEO

def get_lisa_serializer(data, context):

    if 'ts_selected' in data:
        ts_selected = data['ts_selected']

        if ts_selected:
            serializer = CorrelationSerializer(data=data, context=context)

            # check which correlation was provided
            if 'correlation_algorithm' in data:
                correlation_algorithm = data['correlation_algorithm']

                if correlation_algorithm:
                    if correlation_algorithm == PEARSON:
                        serializer = PearsonSerializer(data=data, context=context)

                    elif correlation_algorithm == DTW:
                        serializer = DTWPearsonSerializer(data=data, context=context)

                    elif correlation_algorithm == GEO:
                        serializer = GeographicDistanceSerializer(data=data, context=context)
                else:
                    serializer = CorrelationSerializer(data=data, context=context)
        else:
            serializer = TSSerializer(data=data, context=context)
    else:
        serializer = TSSerializer(data=data, context=context)

    return serializer
