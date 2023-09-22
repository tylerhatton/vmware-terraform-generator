module "example-server-linuxvm" {
  source               = "Terraform-VMWare-Modules/vm/vsphere"
  version              = "3.7.0"
  vmname               = "example-server-linux"
  dc                   = "Datacenter"
  cpu_number           = "2"
  num_cores_per_socket = "2"
  resource_pool        = "Resource Pool name"
  memory               = "2048"
}
