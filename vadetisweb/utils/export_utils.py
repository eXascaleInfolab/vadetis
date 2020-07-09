import csv, json
from django.core.files.temp import NamedTemporaryFile

from .date_utils import *


def export_to_csv(dataset_series_json):
    export_file = NamedTemporaryFile(suffix='.csv')
    series_data = dataset_series_json['series']

    header = ['ts_name', 'time', 'unit', 'value', 'class']
    with open(export_file.name, 'w') as file_output:
        writer = csv.writer(file_output, delimiter=';')
        writer.writerow(header)

        for series in series_data:
            for point in series['data']:
                time = epoch_to_iso8601(point['x'], 'milliseconds')
                row = [series['name'], time, series['unit'], point['y'], point['class']]
                writer.writerow(row)

    return export_file


def export_to_json(dataset_series_json):
    export_file = NamedTemporaryFile(suffix='.json')
    series_data = dataset_series_json['series']
    with open(export_file.name, 'w') as file_output:

        for series in series_data: # exclude some keys
            del series['id']
            del series['is_spatial']

        json.dump(series_data, file_output, indent=4)

    return export_file