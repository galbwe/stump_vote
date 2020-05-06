import os
from unittest.mock import patch, MagicMock

from unittest import TestCase

from api.proxies.civicengine import ApiCaller, CivicEngineApi

class MockApiBase(ApiCaller):
    base_url = "https://api.mock"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.mock_response_path = kwargs['mock_response_path']
        except KeyError as e:
            self.mock_response_path = os.path.abspath(os.path.join(
                os.path.pardir,
                'tests',
                'data',
                'mock_response.json'
            ))

    def get_mock_response(self):
        with open(mock_response_path) as f:
            return json.loads(f.read())
    

class MockApiHeaders(MockApiBase):
    authentication_header = {"x-api-key": "mock-api-key"}


class MockApiValidation(MockApiBase):
    MOCK_RESOURCE = "mock"

    resource_optional_params_map = {
        MOCK_RESOURCE: ("mock_param_1", "mock_param_2")
    }


class TestApiCallerHeaders(TestCase):

    def test_get_headers(self):
        api = MockApiHeaders()
        headers = api._get_headers()
        self.assertEqual(
            headers,
            {"x-api-key": "mock-api-key"}
        )

    def test_no_headers(self):
        api = MockApiBase()
        headers = api._get_headers() 
        self.assertEqual(
            headers,
            dict()
        )

class TestApiCallerParameterValidation(TestCase):

    def test_valid_optional_parameters(self):
        api = MockApiValidation()
        optional_params = [
            dict(),
            {'mock_param_1': 3},
            {'mock_param_2': 'test'},
            {'mock_param_1': None, 'mock_param_2': None}
        ]
        for valid_optional_parameters in optional_params:
            self.assertEqual(
                api._validate_optional_params('mock', valid_optional_parameters),
                None,
                f'Expected mock resource and optional parameters {valid_optional_parameters} to pass validation.'
            )

    def test_invalid_optional_parameters(self):
        api = MockApiValidation()
        optional_params = [
            {'invalid_param': None},
            {'mock_param_1': None, 'invalid_param': None},
            'mock_param_1',
            ('mock_param_1', None),
            4,
        ]
        for invalid_params in optional_params:
            self.assertRaises(ValueError, api._validate_optional_params, 'mock', optional_params)

    def test_no_optional_params_map(self):
        api = MockApiBase()
        self.assertEqual(
            api._validate_optional_params('mock', {'optional_param_1': None}),
            None
        )

    def test_invalid_resource_name(self):
        api = MockApiValidation()
        self.assertEqual(
            api._validate_optional_params('slkdfhjs23', {'optional_param_1': None}),
            None
        )
