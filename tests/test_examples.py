"""
Test the Terraform code in the examples directories.

This test verifies that each example works by executing it.
"""

import pytest
import boto3
import json

from tests.conftest import terraform_apply_and_output

# from tests.conftest import terraform_plan


@pytest.fixture(scope="module")
def output():
    # tf_output_basic is a re-usable test fixture.
    yield from terraform_apply_and_output("examples/basic")


# Execute a test with the tf_output_basic fixture
def test_examples_basic(output):
    # Do nothing else here; but at least TF apply must have run successfully.
    pass


def test_s3_bucket_creation(output):
    # Verify that the bucket was actually created with the specified name
    bucket_name = output["module_example"]["bucket_name"]

    session = boto3.Session()
    s3 = session.client("s3")

    response = s3.list_buckets()
    found = False
    for bucket in response["Buckets"]:
        if bucket["Name"] == bucket_name:
            found = True
    assert found


def test_s3_bucket_encryption(output):
    # Verify that the bucket objects will be encrypted with the correct KMS key
    # Verify that bucket key is enabled to reduce costs
    bucket_name = output["module_example"]["bucket_name"]

    expected_kms_key_id = output["kms_key_arn"]
    apparent_kms_key_id = output["module_example"]["kms_key_id"]
    assert expected_kms_key_id == apparent_kms_key_id

    session = boto3.Session()
    s3 = session.client("s3")

    response = s3.get_bucket_encryption(Bucket=bucket_name)

    rules = response["ServerSideEncryptionConfiguration"]["Rules"]
    assert 1 == len(rules)
    rule = rules[0]

    assert "aws:kms" == rule["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"]

    actual_kms_key_id = rule["ApplyServerSideEncryptionByDefault"]["KMSMasterKeyID"]
    assert actual_kms_key_id == expected_kms_key_id

    assert rule["BucketKeyEnabled"]


def test_s3_bucket_policy(output):
    # Verify that unencrypted communication is denied
    # Verify that the default bucket policy was applied
    bucket_name = output["module_example"]["bucket_name"]

    apparent_bucket_policy = json.loads(
        output["module_example"]["default_bucket_policy_document"]["json"]
    )
    statements = apparent_bucket_policy["Statement"]
    assert 1 == len(statements)
    statement = statements[0]

    assert "DenyUnencryptedCommunication" == statement["Sid"]
    assert "Deny" == statement["Effect"]
    assert "*" == statement["Principal"]["AWS"]
    assert "s3:*" == statement["Action"]

    expected_resources = [
        f"arn:aws:s3:::{bucket_name}",
        f"arn:aws:s3:::{bucket_name}/*",
    ]
    assert set(statement["Resource"]) == set(expected_resources)
    assert "false" == statement["Condition"]["Bool"]["aws:SecureTransport"][0]

    # ### Compare apparent to actual
    # Change ["false"] to "false" so the next comparison passes
    if "false" == statement["Condition"]["Bool"]["aws:SecureTransport"][0]:
        statement["Condition"]["Bool"]["aws:SecureTransport"] = "false"

    apparent_bucket_policy["Statement"] = [statement]
    apparent_bucket_policy = json.dumps(apparent_bucket_policy, sort_keys=True)

    session = boto3.Session()
    s3 = session.client("s3")

    response = s3.get_bucket_policy(Bucket=bucket_name)

    actual_bucket_policy = json.loads(response["Policy"])
    actual_bucket_policy = json.dumps(actual_bucket_policy, sort_keys=True)

    assert actual_bucket_policy == apparent_bucket_policy
