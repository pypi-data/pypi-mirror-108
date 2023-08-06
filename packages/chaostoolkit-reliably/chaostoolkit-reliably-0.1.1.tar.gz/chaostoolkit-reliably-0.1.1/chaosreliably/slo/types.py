from typing import List, Optional

from pydantic import BaseModel, Field

__all__ = ["Reports"]


class SLOWindow(BaseModel):
    from_: str = Field(..., alias='from')
    to_: str = Field(..., alias='to')


class SLOResult(BaseModel):
    delta: float
    actual: float
    slo_is_met: bool


class SLO(BaseModel):
    name: str
    type: str
    period: str
    objective: float
    window: Optional[SLOWindow]
    result: Optional[SLOResult]


class Service(BaseModel):
    name: str
    service_levels: List[SLO]


class Services(BaseModel):
    services: List[Service]
    timestamp: str


class PageInfo(BaseModel):
    cursor: str
    has_next_page: bool


class Reports(BaseModel):
    reports: List[Services]
    page_info: PageInfo
