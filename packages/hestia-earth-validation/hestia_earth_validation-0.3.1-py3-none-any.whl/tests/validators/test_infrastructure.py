import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.infrastructure import validate_lifespan


def test_validate_lifespan_valid():
    with open(f"{fixtures_path}/infrastructure/lifespan/valid.json") as f:
        infrastructure = json.load(f)
    assert validate_lifespan([infrastructure])


def test_validate_lifespan_invalid():
    with open(f"{fixtures_path}/infrastructure/lifespan/invalid.json") as f:
        infrastructure = json.load(f)
    assert validate_lifespan([infrastructure]) == {
        'level': 'error',
        'dataPath': '.infrastructure[0].lifespan',
        'message': 'must equal to endDate - startDate in decimal years (~2.6)'
    }
