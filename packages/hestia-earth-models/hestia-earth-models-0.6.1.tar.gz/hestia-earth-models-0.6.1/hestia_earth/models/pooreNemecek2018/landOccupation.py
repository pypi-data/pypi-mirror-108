from hestia_earth.schema import CycleFunctionalUnitMeasure, IndicatorStatsDefinition
from hestia_earth.utils.tools import list_sum, list_average

from hestia_earth.models.log import logger
from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.impact_assessment import get_product, get_site
from hestia_earth.models.utils.measurement import most_relevant_measurement_value
from . import MODEL

TERM_ID = 'landOccupation'


def _indicator(value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    indicator = _new_indicator(TERM_ID, MODEL)
    indicator['value'] = value
    indicator['statsDefinition'] = IndicatorStatsDefinition.MODELLED.value
    return indicator


def _run(impact_assessment: dict, product_value: float, economic_value: float):
    cycle = impact_assessment.get('cycle', {})
    cycleDuration = cycle.get('cycleDuration', 365)
    site = get_site(impact_assessment)
    fallowCorrection = list_average(
        most_relevant_measurement_value(site.get('measurements', []), 'fallowCorrection', cycle.get('endDate')),
        1
    )
    logger.debug('cycleDuration=%s, fallowCorrection=%s', cycleDuration, fallowCorrection)

    # 1) Account for crop duration (for example multiple crops on a given field in a given year)
    value = 10000 * cycleDuration / 365
    # 2) Account for fallow period in crop production
    value = value * fallowCorrection
    # 3) Reduce the impact by economic value share
    value = value * (economic_value / 100)
    # 4) Divide by product value to estimate land occupation (use) per kg.
    value = value / product_value

    return [_indicator(value)]


def _should_run(impact_assessment: dict):
    functionalUnitMeasure = impact_assessment.get('cycle', {}).get('functionalUnitMeasure')
    product = get_product(impact_assessment)
    product_value = list_sum(product.get('value', [0])) if product else 0
    economic_value = product.get('economicValueShare', 0) if product else 0
    logger.debug('product=%s, economicValueShare=%s', product_value, economic_value)

    should_run = product_value > 0 \
        and economic_value > 0 \
        and functionalUnitMeasure == CycleFunctionalUnitMeasure._1_HA.value
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run, product_value, economic_value


def run(impact_assessment: dict):
    should_run, product_value, economic_value = _should_run(impact_assessment)
    return _run(impact_assessment, product_value, economic_value) if should_run else []
