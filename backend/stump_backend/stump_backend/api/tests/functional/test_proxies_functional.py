
import json
import os
from copy import deepcopy
from operator import itemgetter

from django.test import SimpleTestCase
from requests.exceptions import Timeout
from unittest import skip, skipIf

from ...proxies.civicengine import CivicEngineApi

class AbstractBaseMixin(object):

    def setUp(self):
        # self.resource = "districts"
        self.saved_json = self._get_saved_response()
        assert self.saved_json, f"Error loading saved civic engine response for resource {self.resource}."
        # self.args = []
        # self.optional_params = {
            # "address": "12017+W+Alameda+Pkwy+Lakewood+CO+80228",
        # }
        self.api = CivicEngineApi(timeout=5)
        # self.api_method = self.api.get_districts

    def test_success_response(self):
        try:
            success, response_json = self.api_method(
                *self.args,
                optional_params=self.optional_params
            )
            assert success, (
                f"Error calling get {self.resource}",
                f'\nURL\n\t{self.api.base_url}/{self.resource}{self._query_string}'
                f'\nresponse_code\n\t{response_json["status_code"]}.',
                f'\nresponse_body\n\t{json.dumps(response_json["service_response"], indent=2, default=str)}',
            )
        except Timeout:
            assert False, (
                f"Timeout calling get districts after {self.api.timeout} seconds.",
                f'\nURL\n\t{self.api.base_url}/{self.resource}{self._query_string}',
            )
        self._check_json(response_json)

    def _get_saved_response(self):
        path_to_json = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.path.pardir,
                "data",
                f"{self.resource}.json",
            )
        )
        with open(path_to_json) as f:
            saved_json = json.loads(f.read())
            return saved_json
    
    def _query_string(self):
        if not self.optional_params:
            return ""
        return '?' + "&".join(f'{k}={v}' for (k, v) in self.optional_params.items())


class TestCivicEngineGetCandidatesSuccess(AbstractBaseMixin, SimpleTestCase):

    resource = "candidate"

    def setUp(self):
        super().setUp()
        self.args = [
            1,  # candidate_id
        ]
        self.optional_params = {
            "election_id": 1,
        }
        self.api_method = self.api.get_candidate

    def _check_json(self, response_json):
        self.assertJSONEqual(json.dumps(self.saved_json), response_json)


class TestCivicEngineGetDistrictsSuccess(AbstractBaseMixin, SimpleTestCase):

    resource = "districts" 

    def setUp(self):
        super().setUp()
        self.args = []
        self.optional_params = {
            "address": "12017+W+Alameda+Pkwy+Lakewood+CO+80228",
        }
        self.api_method = self.api.get_districts

    def _check_json(self, response_json):
        saved_json = deepcopy(
            self.saved_json
        )  # so that we do not mess up the instance's state in other tests when deleting timestamp keys
        self.assertIn("timestamp", response_json)
        # example timestamp: 2020-05-01T02:58:11.283642
        self.assertRegexpMatches(
            response_json["timestamp"], r"20\d\d-\d{2}-\d{2}T\d{2}:\d{2}.\d{2}\.\d{6}"
        )
        del saved_json["timestamp"]
        del response_json["timestamp"]
        self.assertJSONEqual(json.dumps(response_json), json.dumps(saved_json))


class TestCivicEngineGetElectionsSuccess(AbstractBaseMixin, SimpleTestCase):

    resource = "elections" 

    def setUp(self):
        super().setUp()
        self.args = []
        self.optional_params = {
            "latitude": 39.7416945,
            "longitude": -104.9883106,
            "start_at": "2018-01-01",
            "end_at": "2019-01-01",
        }
        self.api_method = self.api.get_elections

    def _check_json(self, response_json):
        saved_json = deepcopy(
            self.saved_json
        )  # so that we do not mess up the instance's state in other tests when deleting timestamp keys
        self.assertIn("timestamp", response_json)
        # example timestamp: 2020-05-01T02:58:11.283642
        self.assertRegexpMatches(
            response_json["timestamp"], r"20\d\d-\d{2}-\d{2}T\d{2}:\d{2}.\d{2}\.\d{6}"
        )
        del saved_json["timestamp"]
        del response_json["timestamp"]
        self.assertJSONEqual(json.dumps(response_json), json.dumps(saved_json))


class TestCivicEngineGetMeasuresSuccess(AbstractBaseMixin, SimpleTestCase):

    resource = "measures" 

    def setUp(self):
        super().setUp()
        self.args = []
        self.optional_params = {
            "address": "200+16th+St+Mall+Denver+CO+80202",
            "election_id": 392,  # id for CO primary election
        }
        self.api_method = self.api.get_measures

    def _check_json(self, response_json):
        saved_json = deepcopy(
            self.saved_json
        )  # so that we do not mess up the instance's state in other tests when deleting timestamp keys
        self.assertIn("timestamp", response_json)
        # example timestamp: 2020-05-01T02:58:11.283642
        self.assertRegexpMatches(
            response_json["timestamp"], r"20\d\d-\d{2}-\d{2}T\d{2}:\d{2}.\d{2}\.\d{6}"
        )
        del saved_json["timestamp"]
        del response_json["timestamp"]
        self.assertJSONEqual(json.dumps(response_json), json.dumps(saved_json))


class TestCivicEngineGetNormalizedPositionsSuccess(AbstractBaseMixin, SimpleTestCase):

    resource = "normalized-positions" 

    def setUp(self):
        super().setUp()
        self.args = []
        self.optional_params = dict()
        self.api_method = self.api.get_normalized_positions

    def _check_json(self, response_json):
        self.assertJSONEqual(json.dumps(response_json), json.dumps(self.saved_json))



class TestCivicEngineGetsOfficeHoldersSuccess(AbstractBaseMixin, SimpleTestCase):

    resource = "office-holders" 

    def setUp(self):
        super().setUp()
        self.args = []
        self.optional_params = {
            "address": "200+16th+St+Mall+Denver+CO+80202"
        }
        self.api_method = self.api.get_office_holders

    def _check_json(self, response_json):
        saved_json = deepcopy(
            self.saved_json
        )  # so that we do not mess up the instance's state in other tests when deleting timestamp keys
        self.assertIn("timestamp", response_json)
        # example timestamp: 2020-05-01T02:58:11.283642
        self.assertRegexpMatches(
            response_json["timestamp"], r"20\d\d-\d{2}-\d{2}T\d{2}:\d{2}.\d{2}\.\d{6}"
        )
        del saved_json["timestamp"]
        del response_json["timestamp"]
        self.assertJSONEqual(json.dumps(response_json), json.dumps(saved_json))


class TestCivicEngineGetPollingPlacesSuccess(AbstractBaseMixin, SimpleTestCase):

    resource = "polling_places"  # the underscore is not a typo

    def setUp(self):
        super().setUp()
        self.args = []
        self.optional_params = { 
            "election_id": 392, # CO general election
            "latitude": 39.7416945,
            "longitude": -104.9883106,  
        }
        self.api_method = self.api.get_polling_places

    def _check_json(self, response_json):
        saved_json = deepcopy(
            self.saved_json
        )  # so that we do not mess up the instance's state in other tests when deleting timestamp keys
        self.assertIn("timestamp", response_json)
        # example timestamp: 2020-05-01T02:58:11.283642
        self.assertRegexpMatches(
            response_json["timestamp"], r"20\d\d-\d{2}-\d{2}T\d{2}:\d{2}.\d{2}\.\d{6}"
        )
        del saved_json["timestamp"]
        del response_json["timestamp"]
        self.assertJSONEqual(json.dumps(response_json), json.dumps(saved_json))


class TestCivicEngineGetPositionsSuccess(AbstractBaseMixin, SimpleTestCase):

    resource = "positions" 

    def setUp(self):
        super().setUp()
        self.args = []
        self.optional_params = { 
            "address": "200+16th+St+Mall+Denver+CO+80202",
            "include_candidates": 1,
            "election_date": '2016-11-08',
        }
        self.api_method = self.api.get_positions

    def _check_json(self, response_json):
        saved_json = deepcopy(
            self.saved_json
        )  # so that we do not mess up the instance's state in other tests when deleting timestamp keys
        self.assertIn("timestamp", response_json)
        # example timestamp: 2020-05-01T02:58:11.283642
        self.assertRegexpMatches(
            response_json["timestamp"], r"20\d\d-\d{2}-\d{2}T\d{2}:\d{2}.\d{2}\.\d{6}"
        )
        del saved_json["timestamp"]
        del response_json["timestamp"]
        saved_json["address"] = saved_json["address"].replace(' ', '+')
        self.assertJSONEqual(json.dumps(response_json), json.dumps(saved_json))