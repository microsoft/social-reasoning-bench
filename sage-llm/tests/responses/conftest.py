"""Pytest configuration for response tests."""

import functools

import pytest


def skip_on_auth_error(func):
    """Decorator to skip tests that fail due to authentication errors."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if "AuthenticationError" in type(e).__name__:
                pytest.skip(f"Invalid API credentials: {type(e).__name__}")
            raise

    return wrapper


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items):
    """Wrap all test functions to skip on authentication errors."""
    for item in items:
        if hasattr(item, "obj"):
            item.obj = skip_on_auth_error(item.obj)
