# =============================================================================
# SAMPLE FEATURE FILE TEMPLATE
# =============================================================================
# This is a template demonstrating pytest-bdd feature file conventions.
# Copy and modify for your project's features.
#
# Test Markers (use in conftest.py step definitions):
#   @pytest.mark.unit        - Build-time safe (mocked, no I/O)
#   @pytest.mark.integration - Runtime only (requires DB/services)
#   @pytest.mark.browser     - Runtime only (uses browser tools)
#   @pytest.mark.real_asset  - Runtime only (uses actual files/assets)
#   @pytest.mark.slow        - Decoupled from build (heavy processing)
#   @pytest.mark.heavy       - Decoupled from build (GPU, ML inference)
# =============================================================================

@unit
Feature: Sample Feature
    As a <role/user type>
    I want <capability/feature>
    So that <benefit/value>

    Background:
        Given the system is initialized
        And the input directory exists
        And the output directory exists

    # -------------------------------------------------------------------------
    # HAPPY PATH SCENARIOS (Unit Tests - Build Time)
    # -------------------------------------------------------------------------
    @unit
    Scenario: Basic item processing
        Given a file "sample.txt" exists in the input
        And the file has content "Hello World"
        When the service processes the input
        Then the file should be processed successfully
        And the result should be stored in the output
        And the original file should be removed from the input

    @unit
    Scenario: Duplicate item detection
        Given a file "duplicate.txt" with hash "abc123" exists in the input
        And a file with hash "abc123" already exists in storage
        When the service processes the input
        Then the duplicate should be detected
        And the input file should be removed
        And no new file should be added to storage

    @unit
    Scenario: Naming conflict resolution
        Given a file "report.pdf" exists in the input
        And a different file "report.pdf" already exists in output
        When the service processes the input
        Then a file "report_copy_1.pdf" should exist in output
        And the original output file should be unchanged

    # -------------------------------------------------------------------------
    # EDGE CASE SCENARIOS (Unit Tests - Build Time)
    # -------------------------------------------------------------------------
    @unit
    Scenario: Empty input directory
        Given the input directory is empty
        When the service processes the input
        Then no error should occur
        And the service should report "no items to process"

    @unit
    Scenario: Invalid file format
        Given a file "corrupted.xyz" with invalid format exists in the input
        When the service processes the input
        Then the file should be moved to quarantine
        And an error should be logged

    # -------------------------------------------------------------------------
    # INTEGRATION SCENARIOS (Runtime Tests)
    # -------------------------------------------------------------------------
    @integration
    Scenario: End-to-end processing with database
        Given the database is running
        And the service is started
        And a test item is placed in the input
        When I wait for the service to process
        Then the item should appear in the correct location
        And the database should contain the item metadata
        And the service status should show "OK"

    @integration
    Scenario: Service recovery after database disconnect
        Given the service is running
        And the database connection is interrupted
        When the database connection is restored
        Then the service should resume processing
        And no data should be lost

    # -------------------------------------------------------------------------
    # HEAVY TESTS (Decoupled from Build)
    # -------------------------------------------------------------------------
    @slow @real_asset
    Scenario: Large batch processing
        Given 1000 items exist in the input
        When the service processes all items
        Then each item should be correctly processed
        And processing should complete within 5 minutes

    @slow @real_asset
    Scenario: Large file handling
        Given a 500MB file exists in the input
        When the service processes the file
        Then the file should be processed without memory issues
        And the processing should complete successfully


# =============================================================================
# STEP DEFINITION TEMPLATE (for conftest.py)
# =============================================================================
# Add these step definitions to tests/conftest.py:
#
# from pytest_bdd import given, when, then, parsers, scenarios
#
# # Load all scenarios from this feature file
# scenarios('features/sample.feature')
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
# @given("the output directory exists")
# def output_exists(tmp_output, bdd_context):
#     assert tmp_output.exists()
#     bdd_context["output"] = tmp_output
#
# @given(parsers.parse('a file "{filename}" exists in the input'))
# def file_in_input(bdd_context, create_test_file, filename):
#     file_path = create_test_file(bdd_context["input"], filename)
#     bdd_context["file"] = file_path
#
# @given(parsers.parse('the file has content "{content}"'))
# def file_has_content(bdd_context, content):
#     bdd_context["file"].write_text(content)
#
# @when("the service processes the input")
# def service_processes(bdd_context):
#     # Import and call your service
#     # result = my_service.process(bdd_context["input"])
#     # bdd_context["result"] = result
#     pass
#
# @then("the file should be processed successfully")
# def file_processed(bdd_context):
#     # assert bdd_context["result"].success
#     pass
#
# @then("the result should be stored in the output")
# def result_in_output(bdd_context, tmp_output):
#     # assert (tmp_output / expected_file).exists()
#     pass
# =============================================================================

