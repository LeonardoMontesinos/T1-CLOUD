variable "cluster_name" {
  default = "mi-cluster-fargate"
}

variable "container_name" {
  default = "api-crud"
}

variable "container_port" {
  default = 5000
}

variable "image" {
  default = "310034235193.dkr.ecr.us-east-1.amazonaws.com/api-crud:latest"
}

