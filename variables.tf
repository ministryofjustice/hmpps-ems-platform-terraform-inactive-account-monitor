variable "create" {
  default     = true
  description = "Controls whether resources should be created."
  type        = bool
}

variable "create_package" {
  description = "Controls whether Lambda package should be created. Can be used with var.create=false to ensure the function package builds during CI."
  type        = bool
  default     = true
}

variable "name_prefix" {
  default     = ""
  description = "Prefix to apply to all resource names."
  type        = string
}

variable "report_only" {
  default     = "false"
  description = "Run the lambda without taking any actions, i.e. only report what would happen"
  type        = string
}

variable "schedule" {
  default     = "rate(24 hours)"
  description = "Defines how frequently the users are checked."
  type        = string
}

variable "tags" {
  description = "A map of tags to assign to resources."
  type        = map(string)
  default     = {}
}
