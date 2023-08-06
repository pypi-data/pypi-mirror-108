from chaoslib.exceptions import ActivityFailed
import pytest

from chaosreliably.slo.tolerances import last_N_slo_were_met_for_all_services
from chaosreliably.slo.types import SLO, SLOResult, SLOWindow


def test_last_N_slo_were_met_for_all_services_failed():
    assert last_N_slo_were_met_for_all_services({
        "svc1/latency/slo1": [SLO(
                    name="slo1", type="latency", period="PT1H", objective=99,
                    window=SLOWindow(**{"from":"", "to":""}), result=
                        SLOResult(delta=-50, actual=45, slo_is_met=False)
                ).dict(),
                SLO(
                    name="slo1", type="latency", period="PT1H", objective=99,
                    window=SLOWindow(**{"from":"", "to":""}), result=
                        SLOResult(delta=-50, actual=45, slo_is_met=True)
                ).dict()]
        }) is False


def test_last_N_slo_were_met_for_all_services_met():
    assert last_N_slo_were_met_for_all_services({
        "svc1/latency/slo1": [SLO(
                    name="slo1", type="latency", period="PT1H", objective=99,
                    window=SLOWindow(**{"from":"", "to":""}), result=
                        SLOResult(delta=-50, actual=45, slo_is_met=True)
                ).dict(),
                SLO(
                    name="slo1", type="latency", period="PT1H", objective=99,
                    window=SLOWindow(**{"from":"", "to":""}), result=
                        SLOResult(delta=-50, actual=45, slo_is_met=True)
                ).dict()]
        }) is True