# flake8: noqa
import tftest
import os
import logging
import json


# Resolve to the parent of ./tests
BASE_DIR = os.getcwd()

"""

TEST_SEARCH_CONFIGURATION

Configure an ordered list of places to search for Terraform test code.

The configuration is used to resolve each Python test file, to the Terraform code that tftest will use.
Eg: "test_examples_my_stuff.py" => "examples/my-stuff.py"

Each configuration entry includes:
    - search_path
        Path to some Terraform test code, relative to BASE_DIR.
    - test_namespace (optional)
        Matches to test_NAMESPACE.py or test_NAMESPACE_IDENTIFIER.py
        If unspecified, then test_IDENTIFIER.py could be matched.

The first configuration entry to match a test IDENTIFIER will be used for testing.
"""
TEST_SEARCH_CONFIGURATION = [
    {"search_path": "examples", "test_namespace": "examples"},
    {"search_path": os.path.join("tests", "terraform"), "test_namespace": "terraform"},
]


def terraform_test_search_configuration():
    """Create the final test search configuration from TEST_SEARCH_CONFIGURATION

    The following fields are added:
        - tests_found
            A dictionary of tests that were found, mapping each test identifier to its location:
            test_identifier => location
    """
    configuration = TEST_SEARCH_CONFIGURATION
    # Exclude folders that might not exist
    configuration = [
        c
        for c in configuration
        if os.path.exists(os.path.join(BASE_DIR, c["search_path"]))
    ]
    logging.info("test_search_configuration=%s", configuration)
    # Find all matching test code
    for c, config in enumerate(configuration):
        search_path = config["search_path"]
        sub_directories = [f.name for f in os.scandir(search_path) if f.is_dir()]
        tests_found = {}
        for sd in sub_directories:
            test_identifier = sd.replace("-", "_")
            if test_identifier in tests_found:
                raise Exception(f"Ambiguous test sub-directory {sd} in {search_path}")
            tests_found[test_identifier] = sd
        config["tests_found"] = tests_found
        configuration[c] = config
    return configuration


# Monkeypatch
def _cleanup_github_rubbish(in_):
    """Strip ::debug and ::set-output from the GitHub environment.
    These strings can throw off the test results.
    """
    out = in_
    if in_.find("{"):
        out = in_[in_.find("{") : in_.rfind("}")]
        if out.find("::debug"):
            out = out[: out.find("::debug")]
        if out.find("::set-output"):
            out = out[: out.find("::set-output")]
    return out


def _get_tf_code_location(test_name: str):
    """Return the location of Terraform test code.
    test_name should be either:
     - Python module name, such as 'tests.test_examples_basic'. Requires resolution.
     - Relative path, such as 'examples/basic' or just 'example'. Does not require resolution.
    """
    basedir = BASE_DIR
    if not (test_name.startswith("tests.") or test_name.startswith("test.")):
        # No resolution required, test will be found relative to ../
        tfdir = test_name
        return basedir, tfdir
    # Resolution is required; here we resolve the test.
    # First, change 'tests.test_examples_basic' into 'examples_basic'
    test_identifier = ".".join(test_name.split(".")[1:])
    if test_identifier.startswith("test_"):
        test_identifier = test_identifier[len("test_") :]
    # Determine namespace, eg "examples", if any
    test_namespace = None
    if "_" in test_identifier:
        test_namespace = test_identifier.split("_")[0]
        test_identifier = "_".join(test_identifier.split("_")[1:])
    # Resolve the test
    search_configuration = terraform_test_search_configuration()
    for config in search_configuration:
        if test_namespace == config["test_namespace"]:
            location = config["tests_found"].get(test_identifier)
            if location is not None:
                return config["search_path"], location


def _get_tf(test_name, variables=None):
    """Construct and return `tftest.TerraformTest`, for executing Terraform commands."""
    basedir, tfdir = _get_tf_code_location(test_name)
    logging.info(f"Terraform code located at basedir={basedir} tfdir={tfdir}")
    tf = tftest.TerraformTest(basedir=basedir, tfdir=tfdir)
    # Monkeypatch to avoid github rubbish
    tf._plan_formatter = lambda out: tftest.TerraformPlanOutput(
        json.loads(_cleanup_github_rubbish(out))
    )
    tf._output_formatter = lambda out: tftest.TerraformValueDict(
        json.loads(_cleanup_github_rubbish(out))
    )
    # Populate test.auto.tfvars.json with the specified variables
    variables = variables or {}
    with open(os.path.join(basedir, tfdir, "test.auto.tfvars.json"), "w") as f:
        json.dump(variables, f)
    tf.setup(input=False)
    return tf


def terraform_plan(test_name, variables=None):
    """Run `terraform plan -out`, returning the plan output."""
    tf = _get_tf(test_name, variables=variables)
    yield tf.plan(output=True)


def terraform_apply_and_output(test_name, variables=None):
    """Run `terraform_apply` and then `terraform output`, returning the output."""
    tf = _get_tf(test_name, variables=variables)
    try:
        tf.apply()
        yield tf.output()
    # Shorten the default exception message.
    except tftest.TerraformTestError as e:
        tf.destroy(**{"auto_approve": True})
        raise tftest.TerraformTestError(e.cmd_error) from e
    finally:
        tf.destroy(**{"auto_approve": True})
