# flake8: noqa
import tftest
import os
import logging
import json


def terraform_examples_dir():
    return os.path.join(os.getcwd(), "examples")


def terraform_tests_dir():
    return os.path.join(os.getcwd(), "tests", "terraform")


def terraform_tests():
    """Return a list of tests, i.e subdirectories in `tests/terraform/`."""
    directory = terraform_tests_dir()
    if os.path.isdir(directory):
        return [f.name for f in os.scandir(directory) if f.is_dir()]
    return []


def terraform_examples():
    """Return a list of examples, i.e subdirectories in `examples/`."""
    directory = terraform_examples_dir()
    if os.path.isdir(directory):
        return [f.name for f in os.scandir(directory) if f.is_dir()]
    return []


def terraform_config(terraform_tests, terraform_examples):
    """Convenience fixture for passing around general Terraform config."""
    config = {
        "terraform_tests": terraform_tests,
        "terraform_examples": terraform_examples,
    }
    logging.info(config)
    return config


# Monkeypatch
def _cleanup_github_rubbish(in_):
    out = in_
    if in_.find("{"):
        out = in_[in_.find("{") : in_.rfind("}")]
        if out.find("::debug"):
            out = out[: out.find("::debug")]
        if out.find("::set-output"):
            out = out[: out.find("::set-output")]
    return out


def _get_tf_code_location(test_name):
    basedir = None
    tfdir = test_name
    if "." in tfdir:  # When called with __name__, eg tests.test_examples_basic
        tfdir = test_name.split(".")[-1]
        if tfdir.startswith("test_"):
            tfdir = tfdir[len("test_") :]
    if tfdir.startswith("examples"):
        basedir = terraform_examples_dir()
        tfdir = tfdir[len("examples") + 1 :].replace("_", "-")
    elif tfdir in terraform_config["terraform_tests"]:
        basedir = terraform_tests_dir()
    else:
        raise Exception(f"Unable to locate Terraform code for test {test_name}")
    logging.info(f"{basedir=} {tfdir=}")
    return basedir, tfdir


def _get_tf(test_name, variables=None):
    """Construct and return `tftest.TerraformTest`, for executing Terraform commands."""
    basedir, tfdir = _get_tf_code_location(test_name)
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
    tf.setup()
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
