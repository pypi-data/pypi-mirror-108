from typing import Iterator
from unittest.mock import ANY, patch
from urllib.parse import quote

import pytest
import requests_mock

from sym.flow.cli.errors import NotAuthorizedError, SymAPIUnknownError
from sym.flow.cli.helpers.api import ConnectorType, SymAPI, SymRESTClient
from sym.flow.cli.tests.conftest import get_mock_response

MOCK_INTEGRATIONS_BAD_DATA = [
    {
        "name": "integration 1",
        "type": "aws",
    },
    {
        "name": "integration 2",
        "type": "aws_sso",
    },
]

MOCK_INTEGRATIONS_DATA = [
    {
        "slug": "integration 1",
        "type": "aws",
        "updated_at": "2021-01-19 19:29:46.505678+00",
    },
    {
        "slug": "integration 2",
        "type": "aws_sso",
        "updated_at": "2021-01-19 18:29:46.505678+00",
    },
]

MOCK_SLACK_CONNECTOR_DATA = [
    {
        "type_name": "slack",
        "settings": {
            "team_name": "connector 1",
            "team_id": "T1234567",
            "another_setting": "heyooo",
        },
    },
    {
        "type_name": "slack",
        "settings": {
            "team_name": "connector 2",
            "team_id": "T7654321",
            "another_setting": "porcupines",
        },
    },
]

MOCK_SLACK_CONNECTOR_BAD_DATA = [
    {
        "type_name": "slack",
        "settings": {
            "team_id": "T1234567",
        },
    },
    {
        "type_name": "slack",
        "settings": {
            "team_name": "connector 2",
        },
    },
]


MOCK_BASE_URL = "http://faketest.symops.io/api/v1"


@pytest.fixture
def sym_rest_client(sandbox) -> Iterator[SymRESTClient]:
    with sandbox.push_xdg_config_home():
        yield SymRESTClient(url=MOCK_BASE_URL, access_token="")


@pytest.fixture
def sym_api(sandbox) -> Iterator[SymRESTClient]:
    with sandbox.push_xdg_config_home():
        yield SymAPI(url="http://faketest.symops.io/api/v1", access_token="abc")


class TestSymRESTClient:
    def test_make_headers(self, sym_rest_client, auth_token):
        with pytest.raises(NotAuthorizedError, match="symflow login"):
            sym_rest_client.make_headers()

        sym_rest_client.access_token = "access"
        headers = sym_rest_client.make_headers()
        assert headers.get("X-Sym-Request-ID") is not None
        assert headers.get("Authorization") == "Bearer access"

    def test_process_response(self, sym_rest_client):
        response_500 = get_mock_response(500)
        with pytest.raises(SymAPIUnknownError, match="500"):
            sym_rest_client.process_response(response_500, "abc")

        response_400 = get_mock_response(400)
        with pytest.raises(SymAPIUnknownError, match="400"):
            sym_rest_client.process_response(response_400, "abc")

        response_200 = get_mock_response(200)
        assert sym_rest_client.process_response(response_200, "abc") == (
            response_200,
            "abc",
        )

    @patch(
        "requests.get",
        return_value=get_mock_response(200),
    )
    def test_get(self, mock_requests_get, sym_rest_client):
        params = {"test": "hello"}

        # Auth is required by default, make sure if auth_required not specified
        with pytest.raises(NotAuthorizedError, match="symflow login"):
            sym_rest_client.get("fake-endpoint", params=params)

        mock_requests_get.assert_not_called()

        # If auth_required specified False, we should let the call through
        sym_rest_client.get("fake-endpoint", params=params, auth_required=False)
        mock_requests_get.assert_called_with(
            "http://faketest.symops.io/api/v1/fake-endpoint", params=params, headers=ANY
        )

        # If auth_required not specified False but access token exists, let call through
        sym_rest_client.access_token = "access"
        sym_rest_client.get("fake-endpoint", params=params)
        mock_requests_get.assert_called_with(
            "http://faketest.symops.io/api/v1/fake-endpoint", params=params, headers=ANY
        )

    @patch(
        "requests.delete",
        return_value=get_mock_response(200),
    )
    def test_delete(self, mock_requests_delete, sym_rest_client):
        params = {"test": "hello"}

        # Auth is required by default, make sure if auth_required not specified
        with pytest.raises(NotAuthorizedError, match="symflow login"):
            sym_rest_client.delete("fake-endpoint", params=params)

        mock_requests_delete.assert_not_called()

        # If auth_required specified False, we should let the call through
        sym_rest_client.delete("fake-endpoint", params=params, auth_required=False)
        mock_requests_delete.assert_called_with(
            "http://faketest.symops.io/api/v1/fake-endpoint", params=params, headers=ANY
        )

        # If auth_required not specified False but access token exists, let call through
        sym_rest_client.access_token = "access"
        sym_rest_client.delete("fake-endpoint", params=params)
        mock_requests_delete.assert_called_with(
            "http://faketest.symops.io/api/v1/fake-endpoint", params=params, headers=ANY
        )

    @patch(
        "requests.head",
        return_value=get_mock_response(200),
    )
    def test_head(self, mock_requests_head, sym_rest_client):
        params = {"test": "hello"}

        # Auth is required by default, make sure if auth_required not specified
        with pytest.raises(NotAuthorizedError, match="symflow login"):
            sym_rest_client.head("fake-endpoint", params=params)

        mock_requests_head.assert_not_called()

        # If auth_required specified False, we should let the call through
        sym_rest_client.head("fake-endpoint", params=params, auth_required=False)
        mock_requests_head.assert_called_with(
            "http://faketest.symops.io/api/v1/fake-endpoint", params=params, headers=ANY
        )

        # If auth_required not specified False but access token exists, let call through
        sym_rest_client.access_token = "access"
        sym_rest_client.head("fake-endpoint", params=params)
        mock_requests_head.assert_called_with(
            "http://faketest.symops.io/api/v1/fake-endpoint", params=params, headers=ANY
        )

    @patch(
        "requests.post",
        return_value=get_mock_response(200),
    )
    def test_post(self, mock_requests_post, sym_rest_client):
        params = {"test": "hello"}

        # Auth is required by default, make sure if auth_required not specified
        with pytest.raises(NotAuthorizedError, match="symflow login"):
            sym_rest_client.post("fake-endpoint", params=params, data={})

        mock_requests_post.assert_not_called()

        # If auth_required specified False, we should let the call through
        sym_rest_client.post("fake-endpoint", params=params, auth_required=False, data={})
        mock_requests_post.assert_called_with(
            "http://faketest.symops.io/api/v1/fake-endpoint",
            params=params,
            headers=ANY,
            data=ANY,
        )

        # If auth_required not specified False but access token exists, let call through
        sym_rest_client.access_token = "access"
        sym_rest_client.post("fake-endpoint", params=params, data={})
        mock_requests_post.assert_called_with(
            "http://faketest.symops.io/api/v1/fake-endpoint",
            params=params,
            headers=ANY,
            data=ANY,
        )

    @patch(
        "requests.put",
        return_value=get_mock_response(200),
    )
    def test_put(self, mock_requests_put, sym_rest_client):
        params = {"test": "hello"}

        # Auth is required by default, make sure if auth_required not specified
        with pytest.raises(NotAuthorizedError, match="symflow login"):
            sym_rest_client.put("fake-endpoint", params=params, data={})

        mock_requests_put.assert_not_called()

        # If auth_required specified False, we should let the call through
        sym_rest_client.put("fake-endpoint", params=params, auth_required=False, data={})
        mock_requests_put.assert_called_with(
            "http://faketest.symops.io/api/v1/fake-endpoint",
            params=params,
            headers=ANY,
            data=ANY,
        )

        # If auth_required not specified False but access token exists, let call through
        sym_rest_client.access_token = "access"
        sym_rest_client.put("fake-endpoint", params=params, data={})
        mock_requests_put.assert_called_with(
            "http://faketest.symops.io/api/v1/fake-endpoint",
            params=params,
            headers=ANY,
            data=ANY,
        )

    @patch(
        "requests.patch",
        return_value=get_mock_response(200),
    )
    def test_patch(self, mock_requests_patch, sym_rest_client):
        params = {"test": "hello"}

        # Auth is required by default, make sure if auth_required not specified
        with pytest.raises(NotAuthorizedError, match="symflow login"):
            sym_rest_client.patch("fake-endpoint", params=params, data={})

        mock_requests_patch.assert_not_called()

        # If auth_required specified False, we should let the call through
        sym_rest_client.patch(
            "fake-endpoint", params=params, auth_required=False, data={}
        )
        mock_requests_patch.assert_called_with(
            "http://faketest.symops.io/api/v1/fake-endpoint",
            params=params,
            headers=ANY,
            data=ANY,
        )

        # If auth_required not specified False but access token exists, let call through
        sym_rest_client.access_token = "access"
        sym_rest_client.patch("fake-endpoint", params=params, data={})
        mock_requests_patch.assert_called_with(
            "http://faketest.symops.io/api/v1/fake-endpoint",
            params=params,
            headers=ANY,
            data=ANY,
        )


class TestSymAPI:
    @patch(
        "sym.flow.cli.helpers.api.SymRESTClient.get",
        return_value=(
            get_mock_response(200, data={"client_id": "12345abc", "slug": "test"}),
            "test-request-id",
        ),
    )
    def test_get_organization_from_email(self, mock_api_get, sym_api, test_org):
        email = "test@symops.io"
        org_data = sym_api.get_organization_from_email(email)

        mock_api_get.assert_called_once_with(
            f"login/org-check/{quote(email)}", auth_required=False
        )

        assert org_data["slug"] == test_org["slug"]
        assert org_data["client_id"] == test_org["client_id"]

    @pytest.mark.parametrize("status_code", [400, 403, 500])
    def test_verify_login_failure(self, status_code, sym_api):
        with patch(
            "sym.flow.cli.helpers.api.SymRESTClient.get",
            return_value=(get_mock_response(status_code), "test-request-id"),
        ) as mock_api_get:
            assert sym_api.verify_login("test@symops.io") is False

        mock_api_get.assert_called_once_with(f"login/verify/{quote('test@symops.io')}")

    @pytest.mark.parametrize("status_code", [200])
    def test_verify_login_success(self, status_code, sym_api):
        with patch(
            "sym.flow.cli.helpers.api.SymRESTClient.get",
            return_value=(get_mock_response(status_code), "test-request-id"),
        ) as mock_api_get:
            assert sym_api.verify_login("test@symops.io") is True
        mock_api_get.assert_called_once_with(f"login/verify/{quote('test@symops.io')}")

    @patch(
        "sym.flow.cli.helpers.api.SymRESTClient.get",
        return_value=(
            get_mock_response(200, data=MOCK_SLACK_CONNECTOR_DATA),
            "test-request-id",
        ),
    )
    def test_get_connectors(self, mock_api_get, sym_api):
        data = sym_api.get_connectors(ConnectorType.SLACK.value)
        assert data == MOCK_SLACK_CONNECTOR_DATA

    @patch(
        "sym.flow.cli.helpers.api.SymRESTClient.get",
        return_value=(
            get_mock_response(200, data=MOCK_INTEGRATIONS_DATA),
            "test-request-id",
        ),
    )
    def test_get_integrations(self, mock_api_get, sym_api):
        data = sym_api.get_integrations()
        assert len(data) == 2
        assert data[0]["slug"] == "integration 1"
        assert data[0]["type"] == "aws"
        assert data[0]["updated_at"] == "2021-01-19 19:29:46.505678+00"
        assert data[1]["slug"] == "integration 2"
        assert data[1]["type"] == "aws_sso"
        assert data[1]["updated_at"] == "2021-01-19 18:29:46.505678+00"

    @patch(
        "sym.flow.cli.helpers.api.SymRESTClient.get",
        return_value=(
            get_mock_response(200, data={"url": "http://hello.sym.com"}),
            "test-request-id",
        ),
    )
    def test_get_slack_install_url(self, mock_api_get, sym_api):
        url = sym_api.get_slack_install_url()
        mock_api_get.assert_called_once_with("install/slack/link")
        assert url == "http://hello.sym.com"

    @patch(
        "sym.flow.cli.helpers.api.SymRESTClient.get",
        return_value=(get_mock_response(200), "test-request-id"),
    )
    def test_uninstall_slack(self, mock_api_get, sym_api):
        assert sym_api.uninstall_slack(workspace_id="T1234567") is None
        mock_api_get.assert_called_once_with(
            "uninstall/slack", params={"team_id": "T1234567"}
        )

    def test_get_last_request_id(self, sym_api):
        with requests_mock.Mocker() as m:
            email = "user@example.com"
            m.get(
                f"{MOCK_BASE_URL}/login/org-check/{quote(email)}",
                text='{"slug": "fake-org", "client_id": "fake-client-id"}',
            )

            assert not sym_api.get_last_request_id()
            resp = sym_api.get_organization_from_email(email)
            assert resp["slug"] == "fake-org"
            assert sym_api.get_last_request_id()
