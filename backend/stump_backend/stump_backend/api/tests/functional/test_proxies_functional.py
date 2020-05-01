import json
import os
from operator import itemgetter

from django.test import TestCase
from requests.exceptions import Timeout

from ...proxies.civicengine import CivicEngineApi


class TestLiveCivicEngineApi(TestCase):

    def setUp(self):
        self.data_folder = ''
        self.api = CivicEngineApi(timeout=5)
        # check that responses from the api have been saved to the data folder
        
        # if they have not, set a flag to save data to the folder when it is retrieved

    def tearDown(self):
        pass

    def test_get_districts_success_response(self):
        optional_params = {
            'address': '12017+W+Alameda+Pkwy+Lakewood+CO+80228',
        }
        try:
            success, json_ = self.api.get_districts(optional_params=optional_params)
            assert success, (
                f'Error calling get districts',
                f'\nURL\n\t{self.api.base_url}/districts?address={optional_params["address"]}',
                f'\nresponse_code\n\t{json_["status_code"]}.',
                f'\nresponse_body\n\t{json.dumps(json_["service_response"], indent=2, default=str)}')
        except Timeout:
            assert False, (
                f'Timeout calling get districts after {self.api.timeout} seconds.',
                f'\nURL\n\t{self.api.base_url}/districts?address={optional_params["address"]}',
            )
        # check that the data matches what is saved on disk
        saved_json = self._get_saved_response('districts')
        assert saved_json is not None
        self.assertIn('timestamp', json_)
        # example timestamp: 2020-05-01T02:58:11.283642
        self.assertRegexpMatches(json_['timestamp'], r'20\d\d-\d{2}-\d{2}T\d{2}:\d{2}.\d{2}\.\d{6}')
        self.assertIn('coords', json_)
        self.assertIn('results', json_)
        self.assertEqual(saved_json['coords']['latitude'], json_['coords']['latitude'])
        self.assertEqual(saved_json['coords']['longitude'], json_['coords']['longitude'])
        self.assertEqual(
            sorted(saved_json['results'], key=itemgetter('id')),
            sorted(json_['results'], key=itemgetter('id'))
        )


    def test_get_candidates(self):
        pass

    def test_get_elections(self):
        pass

    def _save_response_to_data_directory(self, response):
        pass

    def _check_data_directory_for_response(self, response):
        pass

    def _get_saved_response(self, resource):
        path_to_json = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            os.path.pardir,
            'data',
            f'{resource}.json'
        ))
        with open(path_to_json) as f:
            saved_json = json.loads(f.read())
            return saved_json

    def _check_api_response_matches_saved_response(self, resources):
        pass
