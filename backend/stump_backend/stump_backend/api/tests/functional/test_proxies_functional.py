import json
import os
from copy import deepcopy
from operator import itemgetter

from django.test import SimpleTestCase
from requests.exceptions import Timeout

from ...proxies.civicengine import CivicEngineApi


class TestCivicEngineDistrictsEndpointSuccess(SimpleTestCase):
    def setUp(self):
        self.resource = 'districts'
        self.saved_json = self._get_saved_response()
        self.args = []
        self.optional_params = {
            'address': '12017+W+Alameda+Pkwy+Lakewood+CO+80228',
        } 
        self.api = CivicEngineApi(timeout=5)

    def test_success_response(self):
        try:
            success, response_json = self.api.get_districts(optional_params=self.optional_params)
            assert success, (
                f'Error calling get districts',
                f'\nURL\n\t{self.api.base_url}/districts?address={self.optional_params["address"]}',
                f'\nresponse_code\n\t{response_json["status_code"]}.',
                f'\nresponse_body\n\t{json.dumps(response_json["service_response"], indent=2, default=str)}')
        except Timeout:
            assert False, (
                f'Timeout calling get districts after {self.api.timeout} seconds.',
                f'\nURL\n\t{self.api.base_url}/districts?address={self.optional_params["address"]}',
            )
        self._check_json(response_json)

    def _get_saved_response(self):
            path_to_json = os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                os.path.pardir,
                'data',
                f'{self.resource}.json'
            ))
            with open(path_to_json) as f:
                saved_json = json.loads(f.read())
                return saved_json

    def _check_json(self, response_json):
        saved_json = deepcopy(self.saved_json)  # so that we do not mess up the instances state in other tests when deleting timestamp keys
        self.assertIn('timestamp', response_json)
        # example timestamp: 2020-05-01T02:58:11.283642
        self.assertRegexpMatches(response_json['timestamp'], r'20\d\d-\d{2}-\d{2}T\d{2}:\d{2}.\d{2}\.\d{6}')
        del saved_json['timestamp']
        del response_json['timestamp']
        self.assertJSONEqual(json.dumps(response_json), json.dumps(saved_json))

    
class TestLiveCivicEngineApi(SimpleTestCase):

    def setUp(self):
        self.data_folder = ''
        self.api = CivicEngineApi(timeout=5)
        # check that responses from the api have been saved to the data folder
        
        # if they have not, set a flag to save data to the folder when it is retrieved

    def tearDown(self):
        pass

    def test_get_candidates_success_response(self):
        candidate_id = 1
        optional_params = {
            'election_id': 1 
        }
        try:
            success, json_ = self.api.get_candidate(candidate_id, optional_params=optional_params)
            assert success, (
                f'Error calling get candidate',
                f'\nURL\n\t{self.api.base_url}/candidate/1?election_id={optional_params["election_id"]}',
                f'\nresponse_code\n\t{json_["status_code"]}.',
                f'\nresponse_body\n\t{json.dumps(json_["service_response"], indent=2, default=str)}')
        except Timeout:
            assert False, (
                f'Timeout calling get districts after {self.api.timeout} seconds.',
                f'\nURL\n\t{self.api.base_url}/candidate/1?election_id={optional_params["election_id"]}',
            )
        # check that the data matches what is saved on disk
        saved_json = self._get_saved_response('candidate')
        assert saved_json is not None
        self.assertJSONEqual(json.dumps(json_), json.dumps(saved_json))


    def test_get_elections(self):
        optional_params = {
            'latitude': 39.7416945,
            'longitude': -104.9883106,
            'start_at': '2018-01-01',
            'end_at': '2019-01-01',
        }
        try:
            success, json_ = self.api.get_elections(optional_params=optional_params)
            assert success, (
                f'Error calling get elections',
                f'\nURL\n\t{self.api.base_url}/elections?{"&".join(str(p) + "=" + str(v) for (p, v) in optional_params.items())}'
                f'\nresponse_code\n\t{json_["status_code"]}.',
                f'\nresponse_body\n\t{json.dumps(json_["service_response"], indent=2, default=str)}')
        except Timeout:
            assert False, (
                f'Timeout calling get elections after {self.api.timeout} seconds.',
                f'\nURL\n\t{self.api.base_url}/elections?{"&".join(str(p) + "=" + str(v) for (p, v) in optional_params.items())}'
            )
        # check that the data matches what is saved on disk
        saved_json = self._get_saved_response('elections')
        assert saved_json is not None
        self.assertIn('timestamp', json_)
        # example timestamp: 2020-05-01T02:58:11.283642
        self.assertRegexpMatches(json_['timestamp'], r'20\d\d-\d{2}-\d{2}T\d{2}:\d{2}.\d{2}\.\d{6}')
        del json_['timestamp']
        del saved_json['timestamp']
        self.assertJSONEqual(json.dumps(json_), json.dumps(saved_json))

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
