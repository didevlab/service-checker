import importlib
from typing import List, Tuple
import logging

from .config import ModuleConfig


def load_monitors(
    module_configs: List[ModuleConfig], logger: logging.Logger
) -> List[Tuple[object, ModuleConfig]]:
    monitors: List[Tuple[object, ModuleConfig]] = []

    for config in module_configs:
        if hasattr(config, "enabled") and not config.enabled:
            logger.info(
                "module disabled via env",
                extra={
                    "event": "module_skip",
                    "module_id": config.slug,
                },
            )
            continue

        module_path = f"app.modules.{config.slug}.monitor"
        try:
            loaded_module = importlib.import_module(module_path)
            factory = getattr(loaded_module, "get_monitor", None)
            if factory is None:
                raise ImportError(f"missing get_monitor() in {module_path}")
            monitor = factory(config.slug)
            configure = getattr(monitor, "configure", None)
            if callable(configure):
                configure(config)
            monitors.append((monitor, config))
            logger.info(
                "module loaded",
                extra={
                    "event": "module_load",
                    "module_id": config.slug,
                    "interval_seconds": config.interval_seconds,
                    "timeout_seconds": config.timeout_seconds,
                },
            )
        except Exception as exc:  # noqa: BLE001
            logger.error(
                "failed to load module",
                extra={
                    "event": "module_load",
                    "module_id": config.slug,
                    "status": "ERROR",
                    "reason": str(exc),
                },
            )
    return monitors
