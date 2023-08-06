from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logger
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.measurement import most_relevant_measurement_value
from hestia_earth.models.utils.ecoClimateZone import get_ecoClimateZone_lookup_value
from . import MODEL

TERM_ID = 'co2ToAirOrganicSoilCultivation'
CONVERT_FACTOR = 44 / 120


def _emission(value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = EmissionMethodTier.TIER_1.value
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _run(histosol: float, organic_soil_factor: float, land_use_change: float):
    value = land_use_change * histosol * organic_soil_factor
    return [_emission(value)]


def _get_CO2_factor(eco_climate_zone: str, site_type: str):
    return get_ecoClimateZone_lookup_value(eco_climate_zone, 'CO2_FACTOR_ORGANIC_SOILS', site_type) * CONVERT_FACTOR


def _should_run(cycle: dict):
    end_date = cycle.get('endDate')
    site = cycle.get('site', {})
    site_type = site.get('siteType', None)
    measurements = site.get('measurements', [])

    def _get_measurement_content(term_id: str):
        return most_relevant_measurement_value(measurements, term_id, end_date)

    histosol = list_sum(_get_measurement_content('histosol'))
    eco_climate_zone = _get_measurement_content('ecoClimateZone')
    eco_climate_zone = str(eco_climate_zone[0]) if len(eco_climate_zone) > 0 else None
    organic_soil_factor = _get_CO2_factor(eco_climate_zone, site_type) if eco_climate_zone else None
    land_use_change = list_sum(_get_measurement_content('landTransformation20YearAverage'))

    should_run = all([organic_soil_factor, land_use_change, histosol])
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run, histosol, organic_soil_factor, land_use_change


def run(cycle: dict):
    should_run, histosol, organic_soil_factor, land_use_change = _should_run(cycle)
    return _run(histosol, organic_soil_factor, land_use_change) if should_run else []
