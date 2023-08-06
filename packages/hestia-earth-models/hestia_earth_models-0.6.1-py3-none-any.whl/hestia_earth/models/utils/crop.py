from hestia_earth.utils.model import find_primary_product
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.tools import safe_parse_float


def get_crop_grouping(term_id: str):
    lookup = download_lookup('crop.csv', True)
    return get_table_value(lookup, 'termid', term_id, column_name('cropGroupingFAOSTAT'))


def get_N2ON_fertilizer_coeff_from_primary_product(cycle: dict):
    product = find_primary_product(cycle)
    term_id = product.get('term', {}).get('@id') if product else None
    lookup = download_lookup('crop.csv', True)
    percent = get_table_value(lookup, 'termid', term_id, column_name('N2ON_FERT')) if term_id else None
    return safe_parse_float(percent, 0.01)
