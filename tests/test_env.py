"""Smoke test for environment and dependencies."""

import bs4
import httpx
import pytest


def test_dependencies_importable():
    """Verify required libraries can be imported."""
    assert httpx.__version__ is not None
    assert bs4.__version__ is not None


@pytest.mark.asyncio
async def test_asyncio_support():
    """Verify asyncio test runner is functional."""
    assert True
