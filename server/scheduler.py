"""定时园丁:后台线程按间隔自动巡库,审批台每天自动有活水。

配置(.env 或环境变量):
    INSIGHTLOOM_GARDEN_INTERVAL_HOURS=24   # 默认每 24 小时;0 或负数 = 关闭
首次巡库在启动一个完整间隔之后执行(给服务预热,避免开机即跑 LLM)。
"""

from __future__ import annotations

import logging
import threading
import time

from . import config

logger = logging.getLogger("insightloom.scheduler")


def _interval_seconds() -> float:
    try:
        hours = float(config.env("GARDEN_INTERVAL_HOURS", "24"))
    except ValueError:
        hours = 24.0
    return hours * 3600.0


def start() -> threading.Thread | None:
    """启动定时巡库线程;返回线程对象(未启用时返回 None)。"""
    seconds = _interval_seconds()
    if seconds <= 0:
        logger.info("定时巡库已关闭(INSIGHTLOOM_GARDEN_INTERVAL_HOURS<=0)")
        return None

    def loop() -> None:
        while True:
            time.sleep(seconds)
            try:
                from . import gardener

                r = gardener.run_gardener()
                logger.info(
                    "定时巡库完成:%s 篇笔记,%s 条新提案",
                    r.get("total_notes", "?"),
                    r.get("proposals_created", "?"),
                )
            except Exception as e:  # 单次失败不杀线程
                logger.warning("定时巡库失败(下轮重试): %s", e)

    t = threading.Thread(target=loop, daemon=True, name="loom-gardener")
    t.start()
    logger.info("定时园丁已启动:每 %.1f 小时巡库一次", seconds / 3600)
    return t
