import os
import pickle
from unittest.mock import patch, MagicMock
from unittest import TestCase

from api.proxies.civicengine import ApiCaller, CivicEngineApi


class MockApiBase(ApiCaller):
    base_url = "https://api.mock"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.mock_data_dir = kwargs['mock_data_dir']
        except KeyError as e:
            self.mock_data_dir = os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                os.path.pardir,
                'data'
            ))
        self.mock_response_pkl = kwargs.get('mock_response_pkl', 'mock_success_response.pkl')

    def get_mock_response(self):
        try:
            with open(os.path.join(self.mock_data_dir, self.mock_response_pkl), 'rb') as f:
                return pickle.loads(f.read())
        except FileNotFoundError as e:
            raise FileNotFoundError('Pickled mock response not found. Try running script to populate mock data.')

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


class MockApiFetch(MockApiHeaders, MockApiValidation):

    def _get_request(self, full_url, optional_params=None):
        headers = self._get_headers()
        response = self.get_mock_response()
        return response        


class TestApiCallerFetch(TestCase):

    def setUp(self):
        self.expected_responses = dict()
        expected_success_response_pkl = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            os.path.pardir,
            'data',
            'mock_success_response.pkl'
        ))
        with open(expected_success_response_pkl, 'rb') as f:
            self.expected_responses['success'] = pickle.loads(f.read())
            

    def test_success_response(self):
        api = MockApiFetch(mock_response_pkl='mock_success_response.pkl')
        success, json = api.fetch('mock', mock_param_1='testing')
        self.assertTrue(success)
        self.assertEqual(json, self.expected_responses['success'].json())