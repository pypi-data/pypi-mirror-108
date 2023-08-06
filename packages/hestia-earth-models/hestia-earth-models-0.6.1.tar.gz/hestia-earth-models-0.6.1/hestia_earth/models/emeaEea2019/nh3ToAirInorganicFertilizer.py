from functools import reduce
from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition
from hestia_earth.utils.lookup import column_name, download_lookup, get_table_value
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import list_average, list_sum, safe_parse_float

from hestia_earth.models.log import logger
from hestia_earth.models.utils.inorganicFertilizer import get_terms, get_term_lookup, get_NH3_emission_factor
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.measurement import most_relevant_measurement_value
from hestia_earth.models.utils.dataCompleteness import _is_term_type_complete
from . import MODEL

TERM_ID = 'nh3ToAirInorganicFertilizer'
LOOKUP_TABLE = 'region-inorganicFertilizer-fertGroupingNitrogen-breakdown.csv'


def _emission(value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = EmissionMethodTier.TIER_1.value
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _get_country_value(country_id: str, col_name: str):
    lookup = download_lookup(LOOKUP_TABLE, True)
    return safe_parse_float(
        get_table_value(lookup, 'termid', country_id, column_name(col_name)), 1)


def _get_groupings():
    term_ids = get_terms()

    def get_grouping(groupings: dict, term_id: str):
        grouping = get_term_lookup(term_id, 'fertGroupingNitrogen')
        return {**groupings, **({grouping: term_id} if len(grouping) > 0 else {})}

    return reduce(get_grouping, term_ids, {})


def _get_term_value(soilPh: float, temperature: float, country_id: str, grouping: str, term_id: str):
    factor = get_NH3_emission_factor(term_id, soilPh, temperature)
    value = _get_country_value(country_id, grouping)
    logger.debug('grouping=%s, NH3_factor=%s, value=%s', grouping, factor, value)
    return value * factor


def _run(temperature: float, soilPh: float, unspecifiedAsN_value: float, country_id: str):
    # creates a dictionary grouping => term_id with only a single key per group (avoid counting twice)
    groupings = _get_groupings()
    value = list_sum([
        _get_term_value(soilPh, temperature, country_id, grouping, term_id) for grouping, term_id in groupings.items()
    ]) * unspecifiedAsN_value
    return [_emission(value)]


def _get_unspecifiedAsN_value(cycle: dict):
    values = find_term_match(
        cycle.get('inputs', []), 'inorganicNitrogenFertilizerUnspecifiedAsN').get('value', [])
    return [0] if len(values) == 0 and _is_term_type_complete(cycle, {'termType': 'fertilizer'}) else values


def _should_run(cycle: dict):
    end_date = cycle.get('endDate')
    site = cycle.get('site', {})
    measurements = site.get('measurements', [])
    soilPh = most_relevant_measurement_value(measurements, 'soilPh', end_date)
    temperature = most_relevant_measurement_value(measurements, 'temperatureAnnual', end_date)
    temperature = most_relevant_measurement_value(
        measurements, 'temperatureLongTermAnnualMean', end_date) if len(temperature) == 0 else temperature

    unspecifiedAsN_value = _get_unspecifiedAsN_value(cycle)

    country_id = site.get('country', {}).get('@id')
    lookup = download_lookup(LOOKUP_TABLE, True)
    in_lookup = country_id in list(lookup.termid)
    logger.debug('Found lookup data for Term: %s? %s', country_id, in_lookup)

    should_run = len(temperature) > 0 \
        and len(soilPh) > 0 \
        and len(unspecifiedAsN_value) > 0 \
        and in_lookup
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run, list_average(temperature), list_average(soilPh), list_sum(unspecifiedAsN_value), country_id


def run(cycle: dict):
    should_run, temperature, soilPh, unspecifiedAsN_value, country_id = _should_run(cycle)
    return _run(temperature, soilPh, unspecifiedAsN_value, country_id) if should_run else []
