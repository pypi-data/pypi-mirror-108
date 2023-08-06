from hestia_earth.models.log import logger
from hestia_earth.models.utils.measurement import most_relevant_measurement, measurement_value_average
from . import MODEL

MODEL_KEY = 'soilAmendments'


def run(cycle: dict):
    end_date = cycle.get('endDate')
    measurements = cycle.get('site', {}).get('measurements', [])
    soilPh_measurement = most_relevant_measurement(measurements, 'soilPh', end_date)
    soilPh = measurement_value_average(soilPh_measurement)
    is_from_model = 'value' in soilPh_measurement.get('added', []) or 'value' in soilPh_measurement.get('updated', [])
    is_complete = is_from_model and soilPh > 6.5
    logger.info('model=%s, key=%s, is_complete=%s', MODEL, MODEL_KEY, is_complete)
    return is_complete
