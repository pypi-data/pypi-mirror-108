import urllib
import requests

from typing import Optional


class Client(object):
    """
    A Client for interacting with the Anonomatic API
    """

    def __init__(
        self,
        account_id: str,
        api_key: str,
        api_url: Optional[str] = "https://api.anonomatic.com",
        verify: Optional[bool] = True,
    ):
        self.account_id = account_id
        self.api_key = api_key
        self.api_url = api_url
        self.verify = verify
        self.api_token = self._login()

    def __repr__(self):
        return f"AnonomaticClient(account_id='{self.account_id}')"

    def _login(self) -> str:
        """
        Generate an API token by logging in to the API.
        """
        ENDPOINT = "/api/auth/login"
        login_url = urllib.parse.urljoin(self.api_url, ENDPOINT)
        data = {
            "AccountID": self.account_id,
            "ApiKey": self.api_key,
        }
        resp = requests.post(login_url, json=data, verify=self.verify)
        return self._handle_response(resp)["Data"]["Token"]

    def _handle_response(self, resp: requests.Response) -> dict:
        resp.raise_for_status()
        if resp.json()["Success"]:
            return resp.json()
        else:
            error = resp.json()["Error"]["Message"]
            status = resp.json()["Error"]["Status"]
            raise Exception(f"Failed to login {self.account_id} with {status}: {error}")

    def _put(self, url: str, data: dict) -> dict:
        """
        Wrapper for requests.put to automatically adding API token.

        url: Full URL for the request
        data: dictionary of JSON data for the request
        """
        full_url = urllib.parse.urljoin(self.api_url, url)
        headers = {"Authorization": f"Bearer {self.api_token}"}
        resp = requests.put(full_url, headers=headers, json=data, verify=self.verify)
        return self._handle_response(resp)

    def _post(self, url: str, data: dict) -> dict:
        """
        Wrapper for requests.post to automatically adding API token.

        url: Full URL for the request
        data: dictionary of JSON data for the request
        """
        full_url = urllib.parse.urljoin(self.api_url, url)
        headers = {"Authorization": f"Bearer {self.api_token}"}
        resp = requests.post(full_url, headers=headers, json=data, verify=self.verify)
        return self._handle_response(resp)

    def get_poly_id(self, profile_data: dict) -> dict:
        """
        Generate a new poly ID based on provided profile data.

        profile_data: Dict with required keys:
        {
            "SourceSystemKey": "NonNullString",
            "FirstName": "NonNullString",
            "MiddleName": "", # Can be empty string
            "LastName": "NonNullString",
            "Emails": [],  # Can be empty list
            "Phones": [],  # Can be empty list
            "Addresses": [],  # Can be empty list
            "Keys": []  # Can be empty list
        }
        """
        ENDPOINT = "/api/profiles/GetPolyId"
        resp = self._put(ENDPOINT, profile_data)
        return resp["Data"]

    def redact(
        self,
        redact_text: str,
        source_system_key: Optional[str] = None,
        poly_id: Optional[str] = None,
    ) -> dict:
        """
        Redact a body of text based on a source_system_key or poly_id

        redact_text: Body of text to redact PII
        source_system_key, poly_id: Requires one of these. Record to reference for PII when redacting text.
        """
        ENDPOINT = "/api/profiles/RedactText"

        if source_system_key is not None:
            payload = {"SourceSystemKey": source_system_key, "RedactText": redact_text}
        elif poly_id is not None:
            payload = {"PolyId": poly_id, "RedactText": redact_text}
        else:
            raise TypeError(
                "Missing required argument 'source_system_key' or 'poly_id'"
            )
        resp = self._post(ENDPOINT, data=payload)
        return resp["Data"]
