"""Script to load mock response data from the Civic Engine Api

Since pickled response objects from the live api are used to 
construct mock data, it is more secure to get this data
via a script before running unit tests. This helps to avoid 
commiting sensitive data like api keys to a git repository.
"""
import pickle
import os
import requests


TEST_DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir, "data")
)


def load_civic_engine_mock_success_response(
    data_dir: str = TEST_DATA_DIR, filename: str = "mock_success_response.pkl"
) -> None:
    url = "https://api.civicengine.com/positions"
    headers = {"x-api-key": os.environ.get("CIVICENGINE_API_KEY")}
    params = {
        "address": "200+16th+St+Mall+Denver+CO+80202",
        "include_candidates": 1,
        "election_date": "2016-11-08",
    }
    res = requests.get(url, headers=headers, params=params)
    with open(os.path.join(data_dir, filename), "wb") as f:
        f.write(pickle.dumps(res))


if __name__ == "__main__":
    load_civic_engine_mock_success_response()
