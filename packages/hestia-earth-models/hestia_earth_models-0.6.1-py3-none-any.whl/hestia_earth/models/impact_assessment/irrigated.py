from hestia_earth.models.log import logger
from . import MODEL

MODEL_KEY = 'irrigated'


def _run(impact: dict):
    practices = impact.get('cycle', {}).get('practices', [])
    value = next((p for p in practices if p.get('term', {}).get('@id') == 'irrigated'), None) is not None
    logger.info('model=%s, key=%s, value=%s', MODEL, MODEL_KEY, value)
    return value


def _should_run(impact: dict):
    practices = impact.get('cycle', {}).get('practices', [])
    should_run = len(practices) > 0
    logger.info('model=%s, key=%s, should_run=%s', MODEL, MODEL_KEY, should_run)
    return should_run


def run(impact: dict): return _run(impact) if _should_run(impact) else False
