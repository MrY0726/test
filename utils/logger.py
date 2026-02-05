import logging
import os
from datetime import datetime

from config import Config


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def get_logger(name: str = "SeleniumTest") -> logging.Logger:
    """
    获取全局 logger：控制台 + 文件
    - 文件固定输出到 reports/logs/<name>.log（每次运行覆盖，方便找）
    - 同时保留一份带时间戳的历史日志
    """
    log_dir = getattr(Config, "LOG_DIR", "reports/logs/")
    _ensure_dir(log_dir)

    level_name = str(getattr(Config, "LOG_LEVEL", "INFO")).upper()
    level = getattr(logging, level_name, logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    # ✅ 关键：避免重复 handler（pytest/多次导入很常见）
    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 固定文件（覆盖）
    fixed_log_file = os.path.join(log_dir, f"{name}.log")
    fh_fixed = logging.FileHandler(fixed_log_file, mode="w", encoding="utf-8")
    fh_fixed.setLevel(level)
    fh_fixed.setFormatter(fmt)

    # 历史文件（可选，但很有用）
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    hist_log_file = os.path.join(log_dir, f"{name}_{ts}.log")
    fh_hist = logging.FileHandler(hist_log_file, mode="w", encoding="utf-8")
    fh_hist.setLevel(level)
    fh_hist.setFormatter(fmt)

    # 控制台
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(fmt)

    logger.addHandler(fh_fixed)
    logger.addHandler(fh_hist)
    logger.addHandler(ch)

    # ✅ 写一条，确保文件立刻生成 & 你能看到路径
    logger.info("Logger initialized. fixed=%s | hist=%s", fixed_log_file, hist_log_file)

    return logger


# 给外部直接 import 用
logger = get_logger()
