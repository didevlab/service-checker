from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class MonitorStatus(str, Enum):
    OK = "OK"
    ALERT = "ALERT"
    ERROR = "ERROR"


@dataclass
class MonitorResult:
    status: MonitorStatus
    message: str
    reason: Optional[str] = None
    duration_ms: Optional[float] = None
    payload: Optional[Any] = None

