"""
Test the Terraform code in the examples directories.

This test verifies that each example works by executing it.
"""

import pytest

from tests.conftest import terraform_apply_and_output

# from tests.conftest import terraform_plan


@pytest.fixture(scope="module")
def tf_output_basic():
    # tf_output_basic is a re-usable test fixture.
    yield from terraform_apply_and_output("examples/basic")


# Execute a test with the tf_output_basic fixture
def test_examples_basic(tf_output_basic):
    # Do nothing else here; but at least TF apply must have run successfully.
    pass


'''
# Further examples of how to test.
# Delete / modify as you wish.

# Multiple uses of the same fixture will re-use the fixture output
# and will not cause repeated TF applies.

def test_examples_basic2(tf_output_basic):
    # Do nothing else here; but at least TF apply must have run successfully.
    pass

# Example of doing detailed testing against TF output
def test_examples_basic_3(tf_output_basic):
    # Verify that the s3 bucket was actually created with the specified name
    bucket_name = output["module_example"]["aws_s3_bucket"]["bucket"]

    session = boto3.Session(profile_name=profile)
    s3 = session.client("s3")

    response = s3.list_buckets()
    found = False
    for bucket in response["Buckets"]:
        if bucket["Name"] == bucket_name:
            found = True
    assert found
    """

# An example of how to test that TF plan works without doing an actual apply
@pytest.fixture(scope="module")
def tf_plan_advanced():
    yield from terraform_plan("examples/advanced")


def test_examples_advanced_1(tf_plan_advanced):
    # Do nothing else here; but at least TF plan must have run successfully.
    pass

def test_examples_advanced_2(tf_plan_advanced):
    # Do nothing else here; but at least TF plan must have run successfully.
    pass

'''
