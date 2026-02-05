import pytest
from utils.logger import get_logger

@pytest.fixture(scope="session", autouse=True)
def _init_log_session():
    get_logger("pytest")
