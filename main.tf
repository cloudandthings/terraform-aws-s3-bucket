resource "null_resource" "delete_me" {
  triggers = var.tags
}
