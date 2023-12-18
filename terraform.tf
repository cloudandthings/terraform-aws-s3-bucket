# TODO versions.tf or terraform.tf ?
terraform {
  required_version = ">= 0.13.1"

  required_providers {
    aws = {
      source = "hashicorp/aws"
      # V6+ does not exist yet, may contain breaking changes.
      version = "~> 5.0"
    }
    null = { # Delete me
      source  = "hashicorp/null"
      version = "~> 3.1"
    }
  }
}
