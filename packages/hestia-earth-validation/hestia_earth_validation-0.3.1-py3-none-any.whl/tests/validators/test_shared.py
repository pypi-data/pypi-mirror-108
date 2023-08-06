import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.shared import (
    validate_dates, validate_list_dates, validate_list_duplicates,
    validate_list_min_max, validate_country, validate_region, validate_area, validate_coordinates,
    need_validate_coordinates, validate_list_term_percent, validate_empty_fields, validate_linked_source_privacy,
    validate_list_dates_length, validate_date_lt_today, validate_list_date_lt_today, validate_properties_default_value
)


def test_validate_dates():
    assert validate_dates({
        'startDate': '2020-01-01'
    })

    assert validate_dates({
        'endDate': '2020-01-02'
    })

    assert validate_dates({
        'startDate': '2020-01-01',
        'endDate': '2020-01-02'
    })

    assert not validate_dates({
        'startDate': '2020-01-02',
        'endDate': '2020-01-01'
    })


def test_validate_list_dates_length_valid():
    cycle = {
        'emissions': [{
            'value': [1],
            'dates': [1]
        }]
    }
    assert validate_list_dates_length(cycle, 'emissions')


def test_validate_list_dates_length_invalid():
    cycle = {
        'emissions': [{
            'value': [1],
            'dates': [1, 2]
        }]
    }
    assert validate_list_dates_length(cycle, 'emissions') == {
        'level': 'error',
        'dataPath': '.emissions[0].dates',
        'message': 'must contain 1 value'
    }


def test_validate_emissions_dates_valid():
    node = {
        'list': [{
            'startDate': '2020-01-01',
            'endDate': '2020-01-02'
        }]
    }
    assert validate_list_dates(node, 'list')


def test_validate_emissions_dates_invalid():
    node = {
        'list': [{
            'startDate': '2020-01-02',
            'endDate': '2020-01-01'
        }]
    }
    assert validate_list_dates(node, 'list') == {
        'level': 'error',
        'dataPath': '.list[0].endDate',
        'message': 'must be greater than startDate'
    }


def test_validate_list_duplicates_valid():
    node = {
        'list': [{
            'startDate': '2020-01-01',
            'endDate': '2020-01-02',
            'value': 1,
            'nested': [{
                'value': 1
            }]
        }, {
            'startDate': '2020-01-01',
            'endDate': '2020-01-02',
            'value': 2,
            'nested': [{
                'value': 2
            }]
        }]
    }
    assert validate_list_duplicates(node, 'list', ['startDate', 'endDate', 'nested.value'])


def test_validate_list_duplicates_invalid():
    node = {
        'list': [{
            'startDate': '2020-01-01',
            'endDate': '2020-01-02',
            'value': 1,
            'nested': [{
                'value': 1
            }]
        }, {
            'startDate': '2020-01-01',
            'endDate': '2020-01-02',
            'value': 2,
            'nested': [{
                'value': 1
            }, {
                'value': 2
            }]
        }]
    }
    assert validate_list_duplicates(node, 'list', ['startDate', 'endDate', 'nested.value']) == {
        'level': 'error',
        'dataPath': '.list[0]',
        'message': 'Duplicates found. '
        'Please make sure there is only one entry with the same startDate, endDate, nested.value'
    }


def test_validate_list_min_max_valid():
    node = {
        'list': [{
            'min': 10,
            'max': 100
        }]
    }
    assert validate_list_min_max(node, 'list')
    node = {
        'list': [{
            'min': [
                50,
                10
            ],
            'max': [
                60,
                20
            ]
        }]
    }
    assert validate_list_min_max(node, 'list')


def test_validate_list_min_max_invalid():
    node = {
        'list': [{
            'min': 100,
            'max': 10
        }]
    }
    assert validate_list_min_max(node, 'list') == {
        'level': 'error',
        'dataPath': '.list[0].max',
        'message': 'must be greater than min'
    }
    node = {
        'list': [{
            'min': [1, 120],
            'max': [10, 20]
        }]
    }
    assert validate_list_min_max(node, 'list') == {
        'level': 'error',
        'dataPath': '.list[0].max',
        'message': 'must be greater than min'
    }


def test_validate_country_valid():
    node = {
        'country': {
            '@id': 'GADM-AUS',
            'name': 'Australia'
        }
    }
    assert validate_country(node)
    node['country']['@id'] = 'region-world'
    assert validate_country(node)


def test_validate_country_invalid():
    node = {
        'country': {
            '@id': 'random-term',
            'name': 'Random'
        }
    }
    assert validate_country(node) == {
        'level': 'error',
        'dataPath': '.country',
        'message': 'must be a country'
    }


def test_validate_region_valid():
    node = {
        'country': {
            '@id': 'GADM-AUS',
            'name': 'Australia'
        },
        'region': {
            '@id': 'GADM-AUS.1_1'
        }
    }
    assert validate_region(node)


def test_validate_region_invalid():
    node = {
        'country': {
            '@id': 'GADM-AUS',
            'name': 'Australia'
        },
        'region': {
            '@id': 'GADM-FRA.1_1'
        }
    }
    assert validate_region(node) == {
        'level': 'error',
        'dataPath': '.region',
        'message': 'must be within the country',
        'params': {
            'country': 'Australia'
        }
    }


def test_validate_area_valid():
    with open(f"{fixtures_path}/shared/area/valid.json") as f:
        node = json.load(f)
    assert validate_area(node)

    # will return valid if the geojson is malformed
    del node['boundary']['features'][0]['type']
    assert validate_area(node)


def test_validate_area_invalid():
    with open(f"{fixtures_path}/shared/area/invalid.json") as f:
        node = json.load(f)
    assert validate_area(node) == {
        'level': 'error',
        'dataPath': '.area',
        'message': 'must be equal to boundary (~13.8)'
    }


def test_validate_coordinates_valid():
    with open(f"{fixtures_path}/shared/coordinates/valid.json") as f:
        node = json.load(f)
    assert validate_coordinates(node)


def test_validate_coordinates_invalid():
    with open(f"{fixtures_path}/shared/coordinates/invalid.json") as f:
        node = json.load(f)
    assert validate_coordinates(node) == {
        'level': 'error',
        'dataPath': '.country',
        'message': 'does not contain latitude and longitude',
        'params': {
            'gadmId': 'GADM-GBR'
        }
    }


def test_need_validate_coordinates():
    node = {}
    assert not need_validate_coordinates(node)

    node['latitude'] = 0
    node['longitude'] = 0
    assert need_validate_coordinates(node)


def test_validate_list_term_percent_valid():
    with open(f"{fixtures_path}/shared/unit-percent/valid.json") as f:
        node = json.load(f)
    assert validate_list_term_percent(node, 'measurements')


def test_validate_list_term_percent_invalid():
    with open(f"{fixtures_path}/shared/unit-percent/invalid.json") as f:
        node = json.load(f)
    assert validate_list_term_percent(node, 'measurements') == {
        'level': 'error',
        'dataPath': '.measurements[0].value',
        'message': 'should be between 0 and 100 (percentage)'
    }


def test_validate_list_term_percent_warning():
    with open(f"{fixtures_path}/shared/unit-percent/warning.json") as f:
        node = json.load(f)
    assert validate_list_term_percent(node, 'measurements') == [{
        'level': 'warning',
        'dataPath': '.measurements[0].value',
        'message': 'may be between 0 and 100'
    }, {
        'level': 'warning',
        'dataPath': '.measurements[1].value',
        'message': 'may be between 0 and 100'
    }]


def test_validate_empty_fields_valid():
    node = {
        'value': 'correct string'
    }
    assert validate_empty_fields(node) == []


def test_validate_empty_fields_warning():
    node = {
        'value1': 'N/A',
        'value2': 'no data',
        'test': None
    }
    assert validate_empty_fields(node) == [{
        'level': 'warning',
        'dataPath': '.value1',
        'message': 'may not be empty'
    }, {
        'level': 'warning',
        'dataPath': '.value2',
        'message': 'may not be empty'
    }]


def test_validate_linked_source_privacy_valid():
    node = {
        'source': {
            'type': 'Source',
            'id': '1'
        },
        'dataPrivate': True
    }
    # valid if no connected source
    assert validate_linked_source_privacy(node, 'source', [])

    source = {
        'type': 'Source',
        'id': '1',
        'dataPrivate': True
    }
    assert validate_linked_source_privacy(node, 'source', [source])

    node['dataPrivate'] = False
    source['dataPrivate'] = False
    assert validate_linked_source_privacy(node, 'source', [source])


def test_validate_linked_source_privacy_invalid():
    node = {
        'source': {
            'type': 'Source',
            'id': '1'
        },
        'dataPrivate': False
    }
    source = {
        'type': 'Source',
        'id': '1',
        'dataPrivate': True
    }
    assert validate_linked_source_privacy(node, 'source', [source]) == {
        'level': 'error',
        'dataPath': '.dataPrivate',
        'message': 'should have the same privacy as the related source',
        'params': {
            'dataPrivate': False,
            'source': {
                'dataPrivate': True
            }
        }
    }

    node['dataPrivate'] = True
    source['dataPrivate'] = False
    assert validate_linked_source_privacy(node, 'source', [source]) == {
        'level': 'error',
        'dataPath': '.dataPrivate',
        'message': 'should have the same privacy as the related source',
        'params': {
            'dataPrivate': True,
            'source': {
                'dataPrivate': False
            }
        }
    }


def test_validate_date_lt_today_valid():
    key = 'date'
    node = {key: '2000-01-01'}
    assert validate_date_lt_today(node, key)


def test_validate_date_lt_today_invalid():
    key = 'date'
    node = {key: '2500-01-01'}
    assert validate_date_lt_today(node, key) == {
        'level': 'error',
        'dataPath': '.date',
        'message': "must be lower than today's date"
    }


def test_validate_list_date_lt_today_valid():
    node = {
        'list': [
            {
                'date1': '2001-01-01'
            },
            {
                'date2': '2002-01-01'
            }
        ]
    }
    keys = ['date1', 'date2', 'date3']
    assert validate_list_date_lt_today(node, 'list', keys)


def test_validate_list_date_lt_today_invalid():
    node = {
        'list': [
            {
                'date1': '2001-01-01'
            },
            {
                'date2': '2500-01-01'
            }
        ]
    }
    keys = ['date1', 'date2', 'date3']
    assert validate_list_date_lt_today(node, 'list', keys) == {
        'level': 'error',
        'dataPath': '.list[1].date2',
        'message': "must be lower than today's date"
    }


def test_validate_properties_default_value_valid():
    with open(f"{fixtures_path}/shared/properties-default-value/valid.json") as f:
        node = json.load(f)
    assert validate_properties_default_value(node, 'inputs', 'properties')


def test_validate_properties_default_value_warning():
    with open(f"{fixtures_path}/shared/properties-default-value/warning.json") as f:
        node = json.load(f)
    assert validate_properties_default_value(node, 'inputs', 'properties') == {
        'level': 'warning',
        'dataPath': '.inputs[0].properties[0].value',
        'message': 'should be within 25% of default value',
        'params': {
            'current': 67.0,
            'default': 52.87673036,
            'delta': 26.71
        }
    }
