"""
Project-wide pytest configuration and pytest-bdd fixtures.

This conftest.py provides:
- Shared fixtures for cross-service integration tests
- pytest-bdd step definitions that apply across all services
- Test markers for two-phase testing strategy

Usage:
    1. Copy this file to your project's tests/ directory
    2. Customize fixtures for your project's needs
    3. Add service-specific fixtures in service test directories
"""
import os
import sys
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

# Add project root to Python path for imports
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =============================================================================
# Test Markers Configuration
# =============================================================================
def pytest_configure(config):
    """Register custom markers for two-phase testing strategy."""
    config.addinivalue_line(
        "markers", "unit: Build-time safe tests (mocked, no I/O, no DB)"
    )
    config.addinivalue_line(
        "markers", "integration: Runtime tests (requires DB, services)"
    )
    config.addinivalue_line(
        "markers", "browser: Runtime tests (uses browser tools)"
    )
    config.addinivalue_line(
        "markers", "real_asset: Runtime tests (uses actual files/assets)"
    )
    config.addinivalue_line(
        "markers", "slow: Decoupled from build (heavy processing, long I/O)"
    )
    config.addinivalue_line(
        "markers", "heavy: Decoupled from build (GPU, ML inference)"
    )


# =============================================================================
# Project-Wide Fixtures
# =============================================================================
@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the project root directory."""
    return PROJECT_ROOT


@pytest.fixture
def tmp_input(tmp_path: Path) -> Path:
    """Create a temporary input directory for testing.
    
    Customize the directory name for your project (e.g., Photos_Inbox, input, data).
    """
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    return input_dir


@pytest.fixture
def tmp_output(tmp_path: Path) -> Path:
    """Create a temporary output directory for testing.
    
    Customize the path structure for your project.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True)
    return output_dir


@pytest.fixture
def mock_database_session():
    """
    Create a mock database session for unit tests.
    
    Use this fixture to avoid database connections in build-time tests.
    Customize for your ORM (SQLAlchemy, Django ORM, Prisma, etc.).
    """
    mock_session = MagicMock()
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=None)
    mock_session.commit = MagicMock()
    mock_session.rollback = MagicMock()
    mock_session.close = MagicMock()
    mock_session.query = MagicMock(return_value=mock_session)
    mock_session.filter = MagicMock(return_value=mock_session)
    mock_session.first = MagicMock(return_value=None)
    mock_session.add = MagicMock()
    return mock_session


@pytest.fixture
def mock_external_service():
    """
    Create a mock external service client for unit tests.
    
    Customize for your external dependencies (Docker, AWS, APIs, etc.).
    """
    mock_client = MagicMock()
    # Add common mock behaviors
    mock_client.is_connected = True
    mock_client.status = "healthy"
    return mock_client


# =============================================================================
# pytest-bdd Fixtures (for Gherkin feature files)
# =============================================================================
try:
    from pytest_bdd import given, when, then, parsers
    
    @pytest.fixture
    def bdd_context():
        """
        Shared context dictionary for passing data between BDD steps.
        
        Usage in step definitions:
            @given("an item exists in the input")
            def item_in_input(bdd_context, tmp_input):
                bdd_context["item_path"] = tmp_input / "test_item"
                # ... create item ...
            
            @when("the service processes the input")
            def service_processes(bdd_context):
                # ... process ...
                bdd_context["result"] = result
            
            @then("the item should be processed")
            def item_processed(bdd_context):
                assert bdd_context["result"].success
        """
        return {}

except ImportError:
    # pytest-bdd not installed, skip BDD fixtures
    pass


# =============================================================================
# Test File Creation Helpers
# =============================================================================
@pytest.fixture
def create_test_file():
    """
    Factory fixture to create test files with specific content.
    
    Returns a function that creates files and optionally sets modification time.
    """
    def _create_file(
        location: Path,
        filename: str,
        content: bytes = b"test file content",
        mtime: float | None = None
    ) -> Path:
        """
        Create a test file.
        
        Args:
            location: Directory where file should be created
            filename: Name of the file
            content: File content (default: "test file content")
            mtime: Modification time as Unix timestamp (default: current time)
        
        Returns:
            Path to created file
        """
        file_path = location / filename
        file_path.write_bytes(content)
        
        if mtime is not None:
            os.utime(file_path, (mtime, mtime))
        
        return file_path
    
    return _create_file


# =============================================================================
# Sample Step Definitions (uncomment and customize)
# =============================================================================
# Add these step definitions for your feature files:
#
# from pytest_bdd import given, when, then, parsers, scenarios
#
# # Load all scenarios from feature files
# scenarios('features/')
#
# @given("the system is initialized")
# def system_initialized(bdd_context):
#     bdd_context["initialized"] = True
#
# @given("the input directory exists")
# def input_exists(tmp_input, bdd_context):
#     assert tmp_input.exists()
#     bdd_context["input"] = tmp_input
#
# @given(parsers.parse('a file "{filename}" exists in the input'))
# def file_in_input(bdd_context, create_test_file, filename):
#     file_path = create_test_file(bdd_context["input"], filename)
#     bdd_context["file"] = file_path
#
# @when("the service processes the input")
# def service_processes(bdd_context):
#     # Call your service
#     result = some_service.process(bdd_context["input"])
#     bdd_context["result"] = result
#
# @then("the file should be processed successfully")
# def file_processed(bdd_context):
#     assert bdd_context["result"].success

