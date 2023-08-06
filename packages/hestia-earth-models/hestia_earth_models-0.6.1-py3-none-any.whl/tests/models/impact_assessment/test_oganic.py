import json
from tests.utils import fixtures_path

from hestia_earth.models.impact_assessment.organic import _should_run, run

fixtures_folder = f"{fixtures_path}/impact_assessment/organic"


def test_should_run():
    # no cycle => no run
    impact = {}
    should_run, *args = _should_run(impact)
    assert not should_run

    # with cycle no practices => no run
    cycle = {'practices': []}
    impact['cycle'] = cycle
    should_run, *args = _should_run(impact)
    assert not should_run

    # with practices
    practice = {'term': {}}
    cycle['practices'].append(practice)
    should_run, *args = _should_run(impact)
    assert should_run


def test_run():
    with open(f"{fixtures_folder}/impact-assessment.jsonld", encoding='utf-8') as f:
        impact = json.load(f)

    value = run(impact)
    assert value
