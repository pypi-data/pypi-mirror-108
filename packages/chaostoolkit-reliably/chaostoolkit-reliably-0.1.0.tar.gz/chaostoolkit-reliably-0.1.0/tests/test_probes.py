import pytest
from tempfile import NamedTemporaryFile

from chaoslib.exceptions import ActivityFailed
import requests
import requests_mock
import yaml


from chaosreliably.slo.probes import get_slo_history


def test_get_slo_history_fails():
    with requests_mock.mock() as m:
        m.get(
            "https://reliably.com/api/v1/orgs/default",
            status_code=200,
            json={"id": "1234"})

        m.get(
            "https://reliably.com/api/v1/userinfo",
            status_code=200,
            json={"id": "567"})

        m.get(
            "https://reliably.com/api/v1/orgs/1234/reports/history",
            status_code=400,
            text="Bad Request")

        with pytest.raises(ActivityFailed) as ex:
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
                get_slo_history(5, {
                    "reliably_config_path": f.name
                })


def test_get_slo_history():
    with requests_mock.mock() as m:
        m.get(
            "https://reliably.com/api/v1/orgs/default",
            status_code=200,
            json={"id": "1234"})

        m.get(
            "https://reliably.com/api/v1/userinfo",
            status_code=200,
            json={"id": "567"})

        m.get(
            "https://reliably.com/api/v1/orgs/1234/reports/history",
            status_code=200,
            json={
                "reports": [{
                    "services": [{
                        "name": "my-service",
                        "service_levels": [{
                            "name": "my-slo",
                            "type": "availability",
                            "period": "PT1H",
                            "objective": 99,
                            "window": {
                                "to": "2021-05-18T07:00:35.919739314Z",
                                "from": "2021-05-18T06:00:35.919739314Z"
                            },
                            "result": {
                                "slo_is_met": True, "actual": 100, "delta": 1
                            }
                        }]
                    }],
                    "timestamp": "2021-05-18T07:00:02.16630444Z"
                }],
                "page_info": {
                    "cursor": "next",
                    "has_next_page": False
                }
            }
        )

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
            get_slo_history(5, {
                "reliably_config_path": f.name
            })
