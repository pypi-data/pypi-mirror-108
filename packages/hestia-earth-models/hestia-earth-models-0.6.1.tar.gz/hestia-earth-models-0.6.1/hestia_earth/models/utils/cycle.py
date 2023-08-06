from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import list_average, list_sum

from . import _filter_list_term_type
from .dataCompleteness import _is_term_type_complete
from .input import get_total_nitrogen


def get_land_occupation(cycle: dict):
    measurements = cycle.get('site', {}).get('measurements', [])
    fallowCorrection = find_term_match(measurements, 'fallowCorrection').get('value', [])
    return cycle.get('cycleDuration', 365) / 365 * list_average(fallowCorrection) if len(fallowCorrection) > 0 else None


def get_excreta_N_total(cycle: dict) -> float:
    """
    Get the total nitrogen content of excreta used in the Cycle.

    The result is the sum of every excreta specified in `kg N` as an `Input` or a `Product`.

    Note: in the event where `dataCompleteness.products` is set to `True` and there are no excreta inputs or products,
    `0` will be returned.

    Parameters
    ----------
    cycle : dict
        The `Cycle` as defined in the Hestia Schema.

    Returns
    -------
    float
        The total value as a number.
    """
    inputs = _filter_list_term_type(cycle.get('inputs', []), TermTermType.EXCRETA)
    products = _filter_list_term_type(cycle.get('products', []), TermTermType.EXCRETA)
    values = get_total_nitrogen(inputs) + get_total_nitrogen(products)
    return 0 if len(values) == 0 and _is_term_type_complete(cycle, {'termType': 'products'}) else list_sum(values)
