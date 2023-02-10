######################################################################
## General access
######################################################################

data "aws_iam_policy_document" "deny_unencrypted_policy_document" {

  statement {
    sid = "DenyUnencryptedCommunication"
    actions = [
      "s3:*"
    ]
    effect = "Deny"
    principals {
      identifiers = [
        "*"
      ]
      type = "AWS"
    }
    resources = [
      aws_s3_bucket.this.arn,
      "${aws_s3_bucket.this.arn}/*"
    ]
    condition {
      test     = "Bool"
      values   = [false]
      variable = "aws:SecureTransport"
    }
  }
}

data "aws_iam_policy_document" "general_read_only_policy_document" {

  statement {
    sid = "GeneralReadOnlyObjectAccess"
    actions = [
      "s3:List*",
      "s3:Get*"
    ]
    effect = "Allow"
    principals {
      identifiers = var.general_read_only_aws_principals
      type        = "AWS"
    }
    resources = [
      aws_s3_bucket.this.arn,
      "${aws_s3_bucket.this.arn}/*"
    ]
  }
}

data "aws_iam_policy_document" "general_read_write_policy_document" {

  statement {
    sid = "GeneralReadWriteObjectAccess"
    actions = [
      "s3:List*",
      "s3:Get*",
      "s3:PutObject",
      "s3:DeleteObject"
    ]
    effect = "Allow"
    principals {
      identifiers = var.general_read_write_aws_principals
      type        = "AWS"
    }
    resources = [
      aws_s3_bucket.this.arn,
      "${aws_s3_bucket.this.arn}/*"
    ]
  }
}

data "aws_iam_policy_document" "default_bucket_policy_document" {
  source_policy_documents = concat(
    [data.aws_iam_policy_document.deny_unencrypted_policy_document.json]
    , length(var.general_read_only_aws_principals) > 0 ? [data.aws_iam_policy_document.general_read_only_policy_document.json] : []
    , length(var.general_read_write_aws_principals) > 0 ? [data.aws_iam_policy_document.general_read_write_policy_document.json] : []
  )
}
