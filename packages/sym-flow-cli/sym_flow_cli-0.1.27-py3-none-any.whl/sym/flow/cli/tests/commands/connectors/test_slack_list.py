from unittest.mock import patch

import pytest

from sym.flow.cli.commands.connectors.slack.slack_list import get_slack_connectors_table
from sym.flow.cli.errors import NotAuthorizedError
from sym.flow.cli.symflow import symflow as click_command
from sym.flow.cli.tests.helpers.test_api import MOCK_SLACK_CONNECTOR_DATA

MOCK_SLACK_CONNECTOR_DATA_STR = """
Workspace Name    Workspace ID
----------------  --------------
connector 1       T1234567
connector 2       T7654321
""".strip()


class TestSlackConnectorList:
    """Suite for testing listing Slack connectors."""

    @patch("sym.flow.cli.commands.connectors.slack.slack_list.click.echo")
    @patch(
        "sym.flow.cli.commands.connectors.slack.slack_list.get_slack_connectors_table",
        return_value="real data",
    )
    def test_click_calls_execution_method(
        self, mock_get_slack_data, mock_click_echo, click_setup
    ):
        with click_setup() as runner:
            result = runner.invoke(click_command, ["connectors", "slack", "list"])
            assert result.exit_code == 0

        mock_get_slack_data.assert_called_once_with("https://api.symops.com/api/v1")
        mock_click_echo.assert_called_once_with("real data")

    @patch(
        "sym.flow.cli.commands.connectors.slack.slack_list.get_slack_connectors_table",
        side_effect=ValueError("random error"),
    )
    def test_click_call_catches_unknown_error(self, mock_get_slack_data, click_setup):
        with click_setup() as runner:
            result = runner.invoke(click_command, ["connectors", "slack", "list"])
            assert result.exit_code == 1
            assert isinstance(result.exception, ValueError)
            assert str(result.exception) == "random error"

        mock_get_slack_data.assert_called_once_with("https://api.symops.com/api/v1")

    @patch(
        "sym.flow.cli.helpers.api.SymAPI.get_connectors",
        side_effect=NotAuthorizedError,
    )
    def test_slack_list_not_authorized_errors(self, mock_get_connectors):
        with pytest.raises(NotAuthorizedError, match="symflow login"):
            get_slack_connectors_table("http://fake.symops.com/api/v1")
        mock_get_connectors.assert_called_once()

    @patch(
        "sym.flow.cli.helpers.api.SymAPI.get_connectors",
        return_value=MOCK_SLACK_CONNECTOR_DATA,
    )
    def test_connectors_slack_list(self, mock_get_connectors):
        data = get_slack_connectors_table("http://fake.symops.com/api/v1")
        assert data == MOCK_SLACK_CONNECTOR_DATA_STR
        mock_get_connectors.assert_called_once()
