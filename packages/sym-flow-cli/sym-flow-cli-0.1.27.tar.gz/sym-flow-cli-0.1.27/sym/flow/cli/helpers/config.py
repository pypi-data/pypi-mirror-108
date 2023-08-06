from typing import Any, Dict, List, Optional, TypedDict, Union

import immutables
from sym.shared.cli.helpers.config.base import ConfigBase

from sym.flow.cli.models import AuthToken, Organization


class ConfigSchema(TypedDict, total=False):
    org: str
    client_id: str
    email: str
    auth_token: AuthToken


def deepget(key: str, data: Dict[str, Any]) -> Optional[str]:
    """Tries to get a nested value from a dict"""
    keys = key.split(".")

    for _key in keys:
        try:
            data = data[_key]
        except KeyError:
            print(f"KeyError for {_key}")
            return None

    if isinstance(data, dict):
        raise ValueError("Value was a dict, not a string")

    if isinstance(data, str):
        return data
    else:
        return None


class Config(ConfigBase[ConfigSchema]):
    @classmethod
    def get_value(cls, key: str) -> Optional[str]:
        config = cls.instance()
        return deepget(key, config)

    @classmethod
    def get_org(cls) -> immutables.Map:
        config = cls.instance()
        return immutables.Map(
            Organization(slug=config["org"], client_id=config["client_id"])
        )

    @classmethod
    def get_access_token(cls) -> str:
        return cls.instance()["auth_token"]["access_token"]

    @classmethod
    def logout(cls):
        if not cls.is_logged_in():
            return

        cfg = cls.instance()
        del cfg["email"]
        del cfg["org"]
        del cfg["client_id"]
        del cfg["auth_token"]


def store_login_config(email: str, org: Organization, auth_token: AuthToken) -> str:
    cfg = Config.instance()
    cfg["email"] = email
    cfg["org"] = org["slug"]
    cfg["client_id"] = org["client_id"]
    cfg["auth_token"] = auth_token
    return str(cfg.file)
