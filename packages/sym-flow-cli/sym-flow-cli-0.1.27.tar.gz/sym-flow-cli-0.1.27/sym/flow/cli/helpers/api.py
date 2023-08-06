import json
import uuid
from enum import Enum
from typing import List, Optional, Tuple
from urllib.parse import quote

import requests
from requests.exceptions import SSLError

from sym.flow.cli.errors import (
    NotAuthorizedError,
    SymAPIMissingEntityError,
    SymAPIRequestError,
    SymAPIUnknownError,
    UnknownOrgError,
)
from sym.flow.cli.helpers.config import Config
from sym.flow.cli.models import Organization


class ConnectorType(Enum):
    SLACK = "slack"


class SymRESTClient:
    """Basic HTTP client for the Sym API."""

    def __init__(self, url: str, access_token: str):
        self.base_url = url
        self.access_token = access_token
        self._last_request_id = ""

    def set_access_token(self, access_token: str):
        self.access_token = access_token

    def make_headers(self, auth_required: bool = True) -> dict:
        """Generates authorization headers."""

        if auth_required and not self.access_token:
            raise NotAuthorizedError

        headers = {"X-Sym-Request-ID": str(uuid.uuid4())}

        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        return headers

    def get_last_request_id(self):
        """Returns the last recorded request ID."""
        return self._last_request_id

    def process_response(
        self,
        response: requests.Response,
        request_id: str,
        validate: bool = True,
    ) -> tuple:
        """Validate a response from the server and raise or return the response and request_id."""
        self._last_request_id = request_id

        if validate and not response.ok:
            for error_class in [SymAPIMissingEntityError]:
                if response.status_code in error_class.error_codes:
                    raise error_class(
                        response_code=response.status_code, request_id=request_id
                    )
            raise SymAPIUnknownError(
                response_code=response.status_code,
                request_id=request_id,
            )

        # Validate that the server returned a valid JSON body
        if validate:
            try:
                response.json()
            except json.decoder.JSONDecodeError as err:
                raise SymAPIRequestError(
                    "The Sym API returned a malformed response.", request_id=request_id
                ) from err

        return response, request_id

    def get(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        validate: bool = True,
        auth_required: bool = True,
    ) -> Tuple[requests.Response, str]:
        """Perform a GET request to the Sym API.

        Returns a tuple of (Response, Request ID) so the Request ID
        can be logged if any errors occur.
        """

        if params is None:
            params = {}

        headers = self.make_headers(auth_required=auth_required)
        request_id = headers["X-Sym-Request-ID"]

        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}", params=params, headers=headers
            )
        except SSLError as err:
            raise SymAPIUnknownError(response_code=0, request_id=request_id) from err

        return self.process_response(response, request_id, validate)

    def patch(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        validate: bool = True,
        auth_required: bool = True,
    ) -> Tuple[requests.Response, str]:
        """Perform a PATCH request to the Sym API.
        Returns a tuple of (Response, Request ID) so the Request ID
        can be logged if any errors occur.
        """

        if params is None:
            params = {}

        headers = self.make_headers(auth_required=auth_required)
        headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        request_id = headers["X-Sym-Request-ID"]

        try:
            response = requests.patch(
                f"{self.base_url}/{endpoint}",
                data=json.dumps(data),
                params=params,
                headers=headers,
            )
        except SSLError as err:
            raise SymAPIUnknownError(response_code=0, request_id=request_id) from err

        return self.process_response(response, request_id, validate)

    def post(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        validate: bool = True,
        auth_required: bool = True,
    ) -> Tuple[requests.Response, str]:
        """Perform a POST request to the Sym API.
        Returns a tuple of (Response, Request ID) so the Request ID
        can be logged if any errors occur.
        """

        if params is None:
            params = {}

        headers = self.make_headers(auth_required=auth_required)
        headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        request_id = headers["X-Sym-Request-ID"]

        try:
            response = requests.post(
                f"{self.base_url}/{endpoint}",
                data=json.dumps(data),
                params=params,
                headers=headers,
            )
        except SSLError as err:
            raise SymAPIUnknownError(response_code=0, request_id=request_id) from err

        return self.process_response(response, request_id, validate)

    def put(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        validate: bool = True,
        auth_required: bool = True,
    ) -> Tuple[requests.Response, str]:
        """Perform a PUT request to the Sym API.
        Returns a tuple of (Response, Request ID) so the Request ID
        can be logged if any errors occur.
        """

        if params is None:
            params = {}

        headers = self.make_headers(auth_required=auth_required)
        headers.update({"Content-Type": "application/json", "Accept": "application/json"})
        request_id = headers["X-Sym-Request-ID"]

        try:
            response = requests.put(
                f"{self.base_url}/{endpoint}",
                data=json.dumps(data),
                params=params,
                headers=headers,
            )
        except SSLError as err:
            raise SymAPIUnknownError(response_code=0, request_id=request_id) from err

        return self.process_response(response, request_id, validate)

    def delete(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        validate: bool = True,
        auth_required: bool = True,
    ) -> Tuple[requests.Response, str]:
        """Perform a DELETE request to the Sym API.

        Returns a tuple of (Response, Request ID) so the Request ID
        can be logged if any errors occur.
        """

        if params is None:
            params = {}

        headers = self.make_headers(auth_required=auth_required)
        request_id = headers["X-Sym-Request-ID"]

        try:
            response = requests.delete(
                f"{self.base_url}/{endpoint}", params=params, headers=headers
            )
        except SSLError as err:
            raise SymAPIUnknownError(response_code=0, request_id=request_id) from err

        return self.process_response(response, request_id, validate)

    def head(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        validate: bool = True,
        auth_required: bool = True,
    ) -> Tuple[requests.Response, str]:
        """Perform a HEAD request to the Sym API.

        Returns a tuple of (Response, Request ID) so the Request ID
        can be logged if any errors occur.
        """

        if params is None:
            params = {}

        headers = self.make_headers(auth_required=auth_required)
        request_id = headers["X-Sym-Request-ID"]

        try:
            response = requests.head(
                f"{self.base_url}/{endpoint}", params=params, headers=headers
            )
        except SSLError as err:
            raise SymAPIUnknownError(response_code=0, request_id=request_id) from err

        return self.process_response(response, request_id, validate)


class SymAPI:
    """Sym API client that implements the client-side of Sym API methods."""

    def __init__(self, url: str, access_token: str = ""):
        if not access_token:
            try:
                access_token = Config.get_access_token()
            except KeyError:  # XXX: This is a terrible way to do it since we are catching a built-in
                # exception but Config.get_access_token() implementation is opaque to us.
                # However, we can't replace it until we fix how Config works.
                # The better way to do this is to have Config.get_access_token()
                # return None instead of letting a built-in exception be raised.
                access_token = None

        self.rest = SymRESTClient(url=url, access_token=access_token)
        self.last_request_id = None

    def set_access_token(self, access_token: str):
        """Set the access token."""
        self.rest.set_access_token(access_token)

    def get_last_request_id(self):
        """Returns the last request ID that was used."""
        return self.rest.get_last_request_id()

    def get_organization_from_email(self, email: str) -> Organization:
        """Exchanges the provided email for the corresponding Organization data."""

        try:
            response, request_id = self.rest.get(
                f"login/org-check/{quote(email)}",
                auth_required=False,
            )
            org_data = response.json()
            return Organization(slug=org_data["slug"], client_id=org_data["client_id"])
        except (KeyError, SymAPIMissingEntityError) as err:
            raise UnknownOrgError(email) from err

    def verify_login(self, email: str) -> bool:
        """Returns True if the User's current credentials are valid for the email provided as determined by the Sym API, False otherwise"""
        response, request_id = self.rest.get(f"login/verify/{quote(email)}")
        return response.status_code == 200

    def get_integrations(self) -> Tuple[List[dict], str]:
        """Retrieve all Sym Integrations accessible to the currently
        authenticated user.
        """
        response, request_id = self.rest.get("integrations/search")
        return response.json()

    def get_users(
        self,
        service_type: Optional[str] = None,
        service: Optional[str] = None,
        include_missing: bool = True,
    ) -> Tuple[List[dict], str]:
        """Retrieve all Sym Users accessible to the currently
        authenticated user.
        Converts retrieved Users' updated_at string to a datetime object
        with the local timezone.
        Returns the list of User data as well as the Request ID for tracking.
        """

        response, request_id = self.rest.get(
            "users/",
            params={
                "service_slugs": [service_type],
                "service_identifiers": [service],
                "include_missing": include_missing,
            },
        )
        return response.json()

    def update_users(self, csv_data: str) -> List[dict]:
        """Patches a set of Users with CSV data."""
        response, request_id = self.rest.patch("users/", data={"csv": csv_data})
        return response.json()

    def get_connectors(self, type_name: Optional[str] = None) -> Tuple[List[dict], str]:
        """Retrieve all Sym Connectors accessible to the currently
        authenticated user.

        Returns the list of integration data as well as the Request ID for tracking.
        """

        params = {}
        if type_name:
            params["type_name"] = type_name

        response, request_id = self.rest.get("connectors/search", params=params)
        return response.json()

    def get_slack_install_url(self) -> Tuple[str, str]:
        """Get the URL that starts the Slack App installation flow.

        Returns:
            The URL to install the Slack App and the Sym Request ID used to
            retrieve the URL as a tuple.
        """

        response, request_id = self.rest.get("install/slack/link")
        return response.json()["url"]

    def uninstall_slack(self, workspace_id: str) -> Tuple[None, str]:
        """Make a request to the Sym API to uninstall the Slack App.

        Raises SymAPIUnknownError from process_response on failure. Otherwise,
        assume success.
        """

        _response, request_id = self.rest.get(
            "uninstall/slack", params={"team_id": workspace_id}
        )

        return None
