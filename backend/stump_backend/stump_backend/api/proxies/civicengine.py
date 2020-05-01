import os
import requests


class ApiCaller(object):
    '''
    High-level wrapper to the Python requests library
    '''

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'base_url'):
            raise ValueError("Missing base_url")
        self.base_url = getattr(self, 'base_url')
        self.timeout = kwargs.get('timeout', 10)

    def _get_headers(self):
        '''
        Returns necessary header needed by the API.
        Currently only the authentication header is set.
        '''
        headers = dict()
        if hasattr(self, 'authentication_header'):
            auth = getattr(self, 'authentication_header')
            for key in auth:
                headers[key] = auth[key]
        return headers

    def _validate_optional_params(self, resource, optional_params):
        '''
        If optional query parameters are passed to the API call, this will
        check that they are contained in a whitelist.
        '''
        if not hasattr(self, 'resource_optional_params_map'):
            return
        resource_optional_params_map = getattr(self, 'resource_optional_params_map')
        if resource not in resource_optional_params_map:
            return
        optional_params_keys = resource_optional_params_map[resource]
        for param in optional_params:
            if param not in optional_params_keys:
                raise ValueError("Optional parameter '{param}' not valid for resource '{resource}'".format(param=param, resource=resource))

    def _get_request(self, full_url, optional_params=None):
        headers = self._get_headers()
        # Makes the actual call to the API
        # TODO: Add error handling, timeouts, and request throttling
        response = requests.get(full_url, headers=headers, params=optional_params, timeout=self.timeout)
        return response

    def fetch(self, resource, *args, **kwargs):
        # Setup optional query parameters
        optional_params = None
        if 'optional_params' in kwargs and kwargs['optional_params'] is not None:
            self._validate_optional_params(resource, kwargs['optional_params'])
            optional_params = kwargs['optional_params']

        # The positional arguments after the resource, e.g. /candidates/1
        positional_args = '/'.join([str(a) for a in args])
        if not positional_args == '':
            # Positional arguements added after slash
            full_url = "{base_url}/{resource}/{positional_args}".format(base_url=self.base_url, resource=resource, positional_args=positional_args)
        else:
            # No postional arguments are use for list queries
            full_url = "{base_url}/{resource}".format(base_url=self.base_url, resource=resource)

        # Make the request
        # TODO: cache the respone, but before implementing caching, check with BallotReady to make sure this complies with our contractual agreement.
        response = self._get_request(full_url, optional_params)
        if response.status_code == requests.codes.ok:
            # Good response
            success = True
            json = response.json()
        else:
            # Something went wrong
            success = False
            json = {'status_code': response.status_code, 'service_response': response.json()}

        # return a tuple with the success flag and the JSON payload
        return success, json


class CivicEngineApi(ApiCaller):
    '''
    Class that encapsulates the calls to BallotRead CivicEngine API.
    See https://developers.civicengine.com/docs/api
    '''

    # Top-level endpoint
    base_url = "https://api.civicengine.com"

    # Setup the API key here
    authentication_header = {'x-api-key': os.getenv('CIVICENGINE_API_KEY')}

    # Resources that are appended to the base_url
    CANDIDATE_RESOURCE = 'candidate'
    DISTRICTS_RESOURCE = 'districts'
    ELECTIONS_RESOURCE = 'elections'
    MEASURES_RESOURCE = 'measures'
    NORMALIZED_POSITIONS_RESOURCE = 'normalized-positions'
    OFFICE_HOLDERS_RESOURCE = 'office-holders'
    POLLING_PLACES_RESOURCE = 'polling_places' 
    POSITIONS_RESOURCE = 'positions' 
    # This whitelist is used for validating the optional parameters
    resource_optional_params_map = {
        CANDIDATE_RESOURCE: ('election_id', 'tenant_id'),
        DISTRICTS_RESOURCE: ('address', 'lat', 'long'),
        ELECTIONS_RESOURCE: ('end_at', 'latitude', 'longitude', 'start_at', 'state', 'updated_since'),
        MEASURES_RESOURCE: ('address', 'lat', 'lng', 'election_id', 'election_date'),  
        NORMALIZED_POSITIONS_RESOURCE: tuple(), 
        OFFICE_HOLDERS_RESOURCE: ('address', 'lat', 'lng'),
        POLLING_PLACES_RESOURCE: ('election_id', 'latitude', 'longitude', 'street_number', 'pre_directional', 'street_name', 'street_suffix', 'post_directional', 'city', 'state', 'zipcode'), 
        POSITIONS_RESOURCE: ('address', 'county', 'election_date', 'election_id', 'exclude_statewide', 'include_candidates', 'include_endorsements', 'include_office_holders', 'include_uncertified_candidates', 'include_volunteer_urls', 'lat', 'level', 'lon', 'search_radius', 'state', 'tier', 'year'), 
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_candidate(self, candidate_id, optional_params=None):
        '''
        GET /candidate/:id
        See https://developers.civicengine.com/docs/api/candidates/by-id
        '''
        result = self.fetch(self.CANDIDATE_RESOURCE, candidate_id, optional_params=optional_params)

        # return the tuple (success, json)
        return result

    def get_districts(self, optional_params=None):
        '''
        GET /districts
        See https://developers.civicengine.com/docs/api/districts/list
        Note: optional_params are not really optiomal. Either address or lat/lon is required.
        '''
        result = self.fetch(self.DISTRICTS_RESOURCE, optional_params=optional_params)

        # return the tuple (success, json)
        return result

    def get_elections(self, optional_params=None):
        '''
        GET /elections
        See https://developers.civicengine.com/docs/api/elections/list
        '''
        result = self.fetch(self.ELECTIONS_RESOURCE, optional_params=optional_params)
        # return the tuple (success, json)
        return result

    def get_measures(self, optional_params=None):
        '''
        GET /elections
        See https://developers.civicengine.com/docs/api/measures/list
        '''
        result = self.fetch(self.MEASURES_RESOURCE, optional_params=optional_params)
        # return the tuple (success, json)
        return result

    def get_normalized_positions(self, optional_params=None):
        '''
        GET /elections
        See https://developers.civicengine.com/docs/api/normalized-positions/list

        '''
        result = self.fetch(self.NORMALIZED_POSITIONS_RESOURCE, optional_params=optional_params)
        # return the tuple (success, json)
        return result

    def get_office_holders(self, optional_params=None):
        '''
        GET /elections
        See https://developers.civicengine.com/docs/api/office-holders/list
        '''
        result = self.fetch(self.OFFICE_HOLDERS_RESOURCE, optional_params=optional_params)
        # return the tuple (success, json)
        return result

    def get_polling_places(self, optional_params=None):
        '''
        GET /elections
        See https://developers.civicengine.com/docs/api/polling_places/list
        '''
        result = self.fetch(self.POLLING_PLACES_RESOURCE, optional_params=optional_params)
        # return the tuple (success, json)
        return result

    def get_positions(self, optional_params=None):
        '''
        GET /elections
        See https://developers.civicengine.com/docs/api/positions/list
        '''
        result = self.fetch(self.POSITIONS_RESOURCE, optional_params=optional_params)
        # return the tuple (success, json)
        return result

