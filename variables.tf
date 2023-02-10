variable "tags" {
  description = "Map of additional tags to assign to created resources. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level."
  type        = map(string)
  default     = {}
}
