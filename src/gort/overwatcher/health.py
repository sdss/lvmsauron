#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2024-12-26
# @Filename: health.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio

from typing import ClassVar

from gort.overwatcher.core import OverwatcherModule, OverwatcherModuleTask
from gort.tools import decap


__all__ = ["HealthOverwatcher"]


class EmitHeartbeatTask(OverwatcherModuleTask["HealthOverwatcher"]):
    """Emits the heartbeat to indicate that the Overwatcher is alive."""

    name = "emit_heartbeat_task"
    keep_alive = True
    restart_on_error = True

    INTERVAL: ClassVar[float] = 5

    def __init__(self):
        super().__init__()

    async def task(self):
        """Sets the overwatcher heartbeat in ``lvmbeat``."""

        while True:
            try:
                cmd = await self.gort.send_command("lvmbeat", "set overwatcher")
                if cmd.status.did_fail:
                    raise RuntimeError("Failed to set overwatcher heartbeat.")

            except Exception as err:
                self.overwatcher.log.error(
                    f"Failed to set overwatcher heartbeat: {decap(err)}",
                    exc_info=err,
                )

            await asyncio.sleep(self.INTERVAL)


class HealthOverwatcher(OverwatcherModule):
    """Monitors health."""

    name = "health"
    tasks = [EmitHeartbeatTask()]
    delay = 0
