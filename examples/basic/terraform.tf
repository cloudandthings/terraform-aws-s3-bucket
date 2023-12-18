terraform {
  required_version = ">= 0.13.1"

  required_providers {
    aws = {
      source = "hashicorp/aws"
      # V5+ does not exist yet, may contain breaking changes.
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.4"
    }
  }
}
