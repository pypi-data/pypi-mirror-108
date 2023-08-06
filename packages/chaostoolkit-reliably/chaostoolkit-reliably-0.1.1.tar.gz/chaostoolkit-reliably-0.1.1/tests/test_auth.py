from tempfile import NamedTemporaryFile

from chaoslib.exceptions import ActivityFailed
import pytest
import yaml

from chaosreliably import get_auth_info


def test_using_config_file():
    with NamedTemporaryFile(mode="w") as f:
        yaml.safe_dump({
            "auths": {
                "reliably.com": {
                    "token": "12345",
                    "username": "jane"
                }
            }
        }, f, indent=2, default_flow_style=False)
        f.seek(0)

        host, token = get_auth_info({
            "reliably_config_path": f.name
        })
        assert token == "12345"
        assert host == "reliably.com"


def test_using_config_file_but_override_token_and_host():
    with NamedTemporaryFile(mode="w") as f:
        yaml.safe_dump({
            "auths": {
                "reliably.com": {
                    "token": "12345",
                    "username": "jane"
                }
            }
        }, f, indent=2, default_flow_style=False)
        f.seek(0)

        host, token = get_auth_info({
            "reliably_config_path": f.name
        }, {
            "reliably": {
                "token": "78890",
                "host": "reliably.dev"
            }
        })
        assert token == "78890"
        assert host == "reliably.dev"


def test_using_secret_only():
    host, token = get_auth_info(None, {
        "reliably": {
            "token": "78890",
            "host": "reliably.dev"
        }
    })
    assert token == "78890"
    assert host == "reliably.dev"


def test_missing_token_from_secrets():
    with pytest.raises(ActivityFailed):
        get_auth_info({
            "reliably_config_path": "",
        }, {
            "reliably": {
                "host": "reliably.dev"
            }
        })


def test_missing_host_from_secrets():
    with pytest.raises(ActivityFailed):
        get_auth_info({
            "reliably_config_path": "",
        }, {
            "reliably": {
                "token": "78890"
            }
        })
