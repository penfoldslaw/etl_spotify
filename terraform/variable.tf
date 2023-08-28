variable "acl_grants" {
  type = list(object({
    type        = string
    permissions = list(string)
  }))
  
  default = [
    {
      type        = "CanonicalUser"
      permissions = ["FULL_CONTROL"]
    }
  ]
}
