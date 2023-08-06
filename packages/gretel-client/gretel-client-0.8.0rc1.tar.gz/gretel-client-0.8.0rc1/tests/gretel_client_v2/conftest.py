import os
from pathlib import Path
from unittest.mock import patch

import pytest

from gretel_client_v2.config import (
    _ClientConfig,
    _load_config,
    configure_session,
)

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def get_fixture():
    def _(name: str) -> Path:
        return FIXTURES / name

    return _


@pytest.fixture(scope="function", autouse=True)
def configure_session_client():
    """Ensures the the host client config is reset after each test."""
    with patch.dict(
        os.environ,
        {
            "GRETEL_API_KEY": os.getenv("GRETEL_API_KEY"),
            "GRETEL_ENDPOINT": "https://api-dev.gretel.cloud",
        },
        clear=True,
    ):
        configure_session(_ClientConfig.from_env())
    yield
    configure_session(_load_config())
