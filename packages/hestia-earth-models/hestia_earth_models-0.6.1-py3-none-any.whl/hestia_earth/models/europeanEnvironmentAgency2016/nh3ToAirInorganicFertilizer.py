from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition, TermTermType
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import list_average, list_sum

from hestia_earth.models.log import logger
from hestia_earth.models.utils import _filter_list_term_type, _filter_list_term_unit
from hestia_earth.models.utils.inorganicFertilizer import get_NH3_emission_factor
from hestia_earth.models.utils.constant import Units
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.measurement import most_relevant_measurement_value
from . import MODEL

TERM_ID = 'nh3ToAirInorganicFertilizer'


def _emission(value: float):
    logger.info('term=%s, value=%s', TERM_ID, value)
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = EmissionMethodTier.TIER_1.value
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _get_input_value(soilPh: float, temperature: float):
    def get_value(input: dict):
        term_id = input.get('term', {}).get('@id')
        factor = get_NH3_emission_factor(term_id, soilPh, temperature)
        logger.debug('factor for Term: %s = %s', term_id, factor)
        return list_sum(input.get('value')) * factor
    return get_value


def _run(temperature: float, soilPh: float, inputs: float):
    value = list_sum(list(map(_get_input_value(soilPh, temperature), inputs)))
    return [_emission(value)]


def _should_run(cycle: dict):
    end_date = cycle.get('endDate')
    site = cycle.get('site', {})
    measurements = site.get('measurements', [])
    soilPh = most_relevant_measurement_value(measurements, 'soilPh', end_date)
    temperature = most_relevant_measurement_value(measurements, 'temperatureAnnual', end_date)
    temperature = most_relevant_measurement_value(
        measurements, 'temperatureLongTermAnnualMean', end_date) if len(temperature) == 0 else temperature

    inputs = _filter_list_term_type(cycle.get('inputs', []), TermTermType.INORGANICFERTILIZER)
    has_unspecified_as_n = find_term_match(inputs, 'inorganicNitrogenFertilizerUnspecifiedAsN', None)

    kg_N_inputs = _filter_list_term_unit(inputs, Units.KG_N)

    should_run = len(temperature) > 0 \
        and len(soilPh) > 0 \
        and not has_unspecified_as_n \
        and len(kg_N_inputs) > 0
    logger.info('term=%s, should_run=%s', TERM_ID, should_run)

    return should_run, list_average(temperature), list_average(soilPh), kg_N_inputs


def run(cycle: dict):
    should_run, temperature, soilPh, inputs = _should_run(cycle)
    return _run(temperature, soilPh, inputs) if should_run else []
