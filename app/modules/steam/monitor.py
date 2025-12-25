import logging
import re
import time
from typing import Optional

import httpx

from ...core.config import ModuleConfig
from ...core.types import MonitorResult, MonitorStatus


class SteamMonitor:
    def __init__(self, slug: str = "steam") -> None:
        self.id = slug
        self.config: Optional[ModuleConfig] = None

    def configure(self, config: ModuleConfig) -> None:
        self.config = config

    async def check(
        self, http_client: httpx.AsyncClient, logger: logging.Logger
    ) -> MonitorResult:
        if self.config is None:
            raise RuntimeError("steam monitor not configured")

        start = time.perf_counter()
        try:
            response = await http_client.get(
                self.config.url,
                timeout=self.config.timeout_seconds,
                headers={"User-Agent": self.config.user_agent},
            )
            body = response.text
        except Exception as exc:  # noqa: BLE001
            duration_ms = (time.perf_counter() - start) * 1000
            return MonitorResult(
                status=MonitorStatus.ERROR,
                message="steam request failed",
                reason=str(exc),
                duration_ms=round(duration_ms, 2),
            )

        duration_ms = (time.perf_counter() - start) * 1000

        if response.status_code >= 400:
            return MonitorResult(
                status=MonitorStatus.ERROR,
            message="steam returned error status",
                reason=f"status {response.status_code}",
                duration_ms=round(duration_ms, 2),
            )

        rule_status, rule_reason, payload = self._evaluate_rule(body)
        if rule_status == MonitorStatus.ERROR:
            return MonitorResult(
                status=MonitorStatus.ERROR,
                message="steam rule evaluation failed",
                reason=rule_reason,
                duration_ms=round(duration_ms, 2),
                payload=payload,
            )

        if rule_status == MonitorStatus.ALERT:
            return MonitorResult(
                status=MonitorStatus.ALERT,
                message="steam indicates outage",
                reason=rule_reason,
                duration_ms=round(duration_ms, 2),
                payload=payload,
            )

        return MonitorResult(
            status=MonitorStatus.OK,
            message="steam reachable",
            duration_ms=round(duration_ms, 2),
            payload=payload,
        )

    def _evaluate_rule(self, body: str) -> tuple[MonitorStatus, Optional[str], Optional[object]]:
        if self.config is None:
            return MonitorStatus.ERROR, "missing config", None

        rule_kind = self.config.rule.kind
        rule_value = self.config.rule.value
        if not rule_value:
            return MonitorStatus.OK, None, None

        if rule_kind == "status":
            return self._evaluate_status_classes(body, rule_value)

        if rule_kind == "keyword":
            if rule_value.lower() in body.lower():
                return MonitorStatus.ALERT, f"keyword '{rule_value}' detected", None
            return MonitorStatus.OK, None, None

        if rule_kind == "regex":
            try:
                pattern = re.compile(rule_value, re.IGNORECASE)
            except re.error as exc:
                return MonitorStatus.ERROR, f"invalid regex: {exc}", None
            if pattern.search(body) is not None:
                return MonitorStatus.ALERT, f"regex '{rule_value}' matched", None
            return MonitorStatus.OK, None, None

        return MonitorStatus.ERROR, f"unsupported rule kind '{rule_kind}'", None

    def _evaluate_status_classes(
        self, body: str, rule_value: str
    ) -> tuple[MonitorStatus, Optional[str], Optional[object]]:
        targets = {item.strip().lower() for item in rule_value.split(",") if item.strip()}
        if not targets:
            targets = {"major", "minor"}

        services = list(_parse_services(body))
        if not services:
            return MonitorStatus.ERROR, "no services found on page", None

        filtered_services = services
        if self.config and self.config.service_filter:
            allow = set(self.config.service_filter)
            filtered_services = [svc for svc in services if svc["id"].lower() in allow]
            if not filtered_services:
                return (
                    MonitorStatus.ERROR,
                    "no target services matched filter",
                    {"services": services, "filter": self.config.service_filter},
                )

        matches = [svc for svc in filtered_services if svc.get("severity") in targets]

        if matches:
            reason = ", ".join(
                f"{svc['name']}: {svc['status_text']} ({svc['severity']})"
                for svc in matches
            )
            return MonitorStatus.ALERT, reason, matches

        return MonitorStatus.OK, None, filtered_services


def _parse_services(body: str):
    service_pattern = re.compile(
        r'<div class="(?:sep )?service">.*?<span class="name">(.*?)</span>.*?'
        r'<span class="status ([^"]+)" id="([^"]+)">(.*?)</span>',
        re.IGNORECASE | re.DOTALL,
    )
    tag_pattern = re.compile(r"<[^>]+>")
    ignored_ids = {"pageviews"}

    for match in service_pattern.finditer(body):
        raw_name = match.group(1)
        status_class = match.group(2)
        status_id = match.group(3).strip().lower()
        status_text = match.group(4).strip()
        if status_id in ignored_ids:
            continue
        # Remove inner HTML (links, svgs) to keep only visible text.
        name = tag_pattern.sub("", raw_name).strip()
        if not name:
            name = "unknown-service"
        class_names = status_class.split()
        severity = next((c for c in class_names if c in {"good", "minor", "major"}), None)
        yield {
            "name": name,
            "class": status_class,
            "id": status_id,
            "severity": severity,
            "status_text": status_text,
        }


def get_monitor(slug: str = "steam") -> SteamMonitor:
    return SteamMonitor(slug=slug)
