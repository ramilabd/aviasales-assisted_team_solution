# -*- coding: utf8 -*-
"""Functional tests of the application."""

import jsonschema
from tests.func_tests.set_json_schemes import (
    flight1_flight2_scheme,
    flight1_scheme,
    min_route_scheme,
    route_scheme,
)


def test_app_airflights(test_client):
    """Check the availability of the web application.

    Args:
        test_client (fixture class flask.testing.FlaskClient): application
            Flask for functionaly testing.
    """
    assert test_client.get('/main_page').status_code == 200


def test_validate_response_all_flights(test_client):
    """Validating the function response.

        Validating the function "receive_all_flights" response for compliance
        with the specified json schema.

    Args:
        test_client (fixture: class flask.testing.FlaskClient): application
            Flask for functionaly testing.
    """
    response_json = test_client.get('/airflights/flights').get_json()

    assert is_corresponds_to_jsonscheme(response_json)


def test_validate_response_json(test_client, get_routes_in_parts):
    """Validating the function response.

        Validating the function "receive_sorted_flights_by_direction" response
        for compliance with the specified json schema.

    Args:
        test_client (fixture: class flask.testing.FlaskClient): application
            Flask for functionaly testing.
        get_routes_in_parts (fixture): Returns each route from the list
            separately. Each route is represented by a dictionary,
            dictionary of the form:
            {'Source': ..., 'Transfer': ..., 'Destination': ...}.
    """
    urls = [
        '/airflights/flights/sorted_by_direction/<source>/<destination>',
        '/airflights/flights/sorted_by_price/<source>/<destination>',
        '/airflights/flights/sorted_by_time/<source>/<destination>',
        '/airflights/flights/optimal_routes/<source>/<destination>',
    ]
    for url in urls:
        for route in get_routes_in_parts():
            response_json = test_client.get(
                url,
                data={
                    'source': route.get('Source'),
                    'destination': route.get('Destination'),
                },
            ).get_json(force=True)

            assert is_corresponds_to_jsonscheme(response_json)


def test_validate_response_get_all_route(test_client):
    """Validating the function response.

        Validating the function "receive_get_all_route" response
        for compliance with the specified json schema.

    Args:
        test_client (fixture: class flask.testing.FlaskClient): application
            Flask for functionaly testing.
    """
    response_json = test_client.get(
        '/airflights/flights/all_routes',
    ).get_json(force=True)

    is_json_valide = True
    for route in response_json:
        if 'Transfer' in route:
            scheme = route_scheme
        else:
            scheme = min_route_scheme

        try:
            jsonschema.validate(route, scheme)
        except jsonschema.exceptions.ValidationError:
            is_json_valide = False

        assert is_json_valide


def is_corresponds_to_jsonscheme(response_json):
    """Validate to the specified scheme.

    Args:
        response_json (json): response of the function.

    Returns:
        bool: True - corresponds to the specified scheme,
            False - does not match the specified scheme.
    """
    is_json_valide = True

    for flight in response_json:
        if flight.get('flight2') is None:
            scheme = flight1_scheme
        else:
            scheme = flight1_flight2_scheme

        try:
            jsonschema.validate(flight, scheme)
        except jsonschema.exceptions.ValidationError:
            is_json_valide = False

    return is_json_valide
